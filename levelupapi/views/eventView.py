"""View module for handling requests about game types"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from levelupapi.models import Event, Gamer, Game
from rest_framework.decorators import action
from django.db.models import Count
from django.db.models import Q


class EventView(ViewSet):
    """Level up events view"""

    def list(self, request):
        """Handle GET requests to get all events

        Returns:
            Response -- JSON serialized list of events
        """

        gamer = Gamer.objects.get(user=request.auth.user)
        events = Event.objects.annotate(
            attendees_count=Count("attendees"),
            joined=Count("attendees", filter=Q(attendees=gamer)),
        )

        serializer = EventSerializer(events, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def retrieve(self, request, pk=None):
        """Handle GET requests for single event

        Returns:
            Response -- JSON serialized event
        """
        try:
            event = Event.objects.get(pk=pk)
            serializer = EventSerializer(event)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Event.DoesNotExist as ex:
            return Response({"message": ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

    def create(self, request):
        """Handle POST operations

        Returns:
            Response -- JSON serialized game instance
        """
        gamer = Gamer.objects.get(user=request.auth.user)
        serializer = CreateEventSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        event = serializer.save(organizer=gamer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, pk):
        """Handle PUT requests for an event

        Returns:
            Response -- Empty body with 204 status code
        """
        event = Event.objects.get(pk=pk)

        event.description = request.data["description"]
        event.date = request.data["date"]
        event.time = request.data["time"]
        organizer = Gamer.objects.get(user=request.auth.user)
        event.organizer = organizer
        event.attendees.clear()
        for attendee_id in request.data["attendees"]:
            attendee = Gamer.objects.get(pk=attendee_id)
            event.attendees.add(attendee)

        event.game = Game.objects.get(pk=request.data["game"])

        event.save()
        serializer = EventSerializer(event)
        return Response(serializer.data)

    def destroy(self, request, pk=None):
        """Handle DELETE requests for events

        Returns:
            Response -- Empty body with 204 status code
        """
        try:
            event = Event.objects.get(pk=pk)
            event.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Event.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    @action(methods=["post"], detail=True)
    def signup(self, request, pk):
        """Post request for a user to sign up for an event"""

        gamer = Gamer.objects.get(user=request.auth.user)
        event = Event.objects.get(pk=pk)
        event.attendees.add(gamer)
        return Response({"message": "Gamer added"}, status=status.HTTP_201_CREATED)

    @action(methods=["delete"], detail=True)
    def leave(self, request, pk):
        """Delete request for a user to leave an event"""

        gamer = Gamer.objects.get(user=request.auth.user)
        event = Event.objects.get(pk=pk)
        event.attendees.remove(gamer)
        return Response({"message": "Gamer deleted"}, status=status.HTTP_204_NO_CONTENT)


class EventSerializer(serializers.ModelSerializer):
    """JSON serializer for events"""

    attendee_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Event
        fields = (
            "id",
            "description",
            "date",
            "time",
            "organizer",
            "attendees",
            "game",
            "joined",
            "attendee_count",
        )
        level = 1


class CreateEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = [
            "id",
            "description",
            "date",
            "time",
            "organizer",
            "attendees",
            "game",
            "joined",
        ]
