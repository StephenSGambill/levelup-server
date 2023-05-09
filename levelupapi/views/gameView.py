"""View module for handling requests about game types"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from levelupapi.models import Game, Gamer, GameType
from django.db.models import Count
from django.db.models import Q
from django.core.exceptions import ValidationError


class GameView(ViewSet):
    """Level up games view"""

    def list(self, request):
        """Handle GET requests to get all games

        Returns:
            Response -- JSON serialized list of games
        """
        gamer = Gamer.objects.get(user=request.auth.user)
        # games = Game.objects.all()
        games = Game.objects.annotate(
            event_count=Count("events"),
            user_event_count=Count("events", filter=Q(gamer=gamer)),
        )

        game_type = request.query_params.get("type", None)

        # check to see if a query string parameter has been passed to the URL
        # filter by game type
        if game_type:
            games = games.filter(game_type_id=game_type)
        if "type" in request.query_params:
            games = games.filter(game_type=game_type)

        serializer = GameSerializer(games, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def retrieve(self, request, pk=None):
        """Handle GET requests for single game

        Returns:
            Response -- JSON serialized game
        """
        gamer = Gamer.objects.get(user=request.auth.user)
        # games = Game.objects.all()
        games = Game.objects.annotate(
            event_count=Count("events"),
            user_event_count=Count("events", filter=Q(gamer=gamer)),
        )

        try:
            game = games.get(pk=pk)
            serializer = GameSerializer(game)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Game.DoesNotExist as ex:
            return Response({"message": ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

    # def create(self, request):
    #     """Handle POST operations

    #     Returns
    #         Response -- JSON serialized game instance
    #     """
    #     # get the user authorization from the token
    #     gamer = Gamer.objects.get(user=request.auth.user)
    #     # get the game type info from database using pk
    #     game_type = GameType.objects.get(pk=request.data["game_type"])

    #     game = Game.objects.create(
    #         title=request.data["title"],
    #         maker=request.data["maker"],
    #         number_of_players=request.data["number_of_players"],
    #         skill_level=request.data["skill_level"],
    #         game_type=game_type,
    #         gamer=gamer,
    #     )
    #     serializer = GameSerializer(game)
    #     return Response(serializer.data)

    def create(self, request):
        """Handle POST operations

        Returns:
            Response -- JSON serialized game instance
        """
        gamer = Gamer.objects.get(user=request.auth.user)
        serializer = CreateGameSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(gamer=gamer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, pk):
        """Handle PUT requests for a game

        Returns:
            Response -- Empty body with 204 status code
        """

        game = Game.objects.get(pk=pk)
        game.title = request.data["title"]
        game.maker = request.data["maker"]
        game.number_of_players = request.data["number_of_players"]
        game.skill_level = request.data["skill_level"]

        game_type = GameType.objects.get(pk=request.data["game_type"])
        game.game_type = game_type
        game.save()

        serializer = GameSerializer(game)
        return Response(serializer.data)

    def destroy(self, request, pk=None):
        """Handle DELETE requests for events
        Returns:
            Response: None with 204 status code
        """
        try:
            game = Game.objects.get(pk=pk)
            game.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Game.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)


class GameSerializer(serializers.ModelSerializer):
    """JSON serializer for games"""

    event_count = serializers.IntegerField(read_only=True)
    user_event_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Game
        fields = (
            "id",
            "title",
            "maker",
            "number_of_players",
            "skill_level",
            "game_type",
            "gamer",
            "event_count",
            "user_event_count",
        )
        depth = 1


class CreateGameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Game
        fields = [
            "id",
            "title",
            "maker",
            "number_of_players",
            "skill_level",
            "game_type",
        ]
