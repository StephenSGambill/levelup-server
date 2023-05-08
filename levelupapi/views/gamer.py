"""View module for handling requests about game types"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from levelupapi.models import Game, Gamer, GameType


class GamerView(ViewSet):
    """Level up games view"""

    def list(self, request):
        """Handle GET requests to get all games

        Returns:
            Response -- JSON serialized list of games
        """

        gamers = Gamer.objects.all()
        serializer = GamerSerializer(gamers, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class GamerSerializer(serializers.ModelSerializer):
    """JSON serializer for games"""

    class Meta:
        model = Gamer
        fields = (
            "id",
            "user",
            "bio",
        )
        depth = 1
