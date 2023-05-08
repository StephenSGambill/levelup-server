"""View module for handling requests about game types"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from levelupapi.models import Game, Gamer, GameType


class GameView(ViewSet):
    """Level up games view"""

    def list(self, request):
        """Handle GET requests to get all games

        Returns:
            Response -- JSON serialized list of games
        """

        games = Game.objects.all()
        serializer = GameSerializer(games, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def retrieve(self, request, pk=None):
        """Handle GET requests for single game

        Returns:
            Response -- JSON serialized game
        """

        game = Game.objects.get(pk=pk)
        serializer = GameSerializer(game)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request):
        """Handle POST operations

        Returns
            Response -- JSON serialized game instance
        """
        # get the user authorization from the token
        gamer = Gamer.objects.get(user=request.auth.user)
        # get the game type info from database using pk
        game_type = GameType.objects.get(pk=request.data["game_type"])

        game = Game.objects.create(
            title=request.data["title"],
            maker=request.data["maker"],
            number_of_players=request.data["number_of_players"],
            skill_level=request.data["skill_level"],
            game_type=game_type,
            gamer=gamer,
        )
        serializer = GameSerializer(game)
        return Response(serializer.data)

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
        game = Game.objects.get(pk=pk)
        game.delete()


class GameSerializer(serializers.ModelSerializer):
    """JSON serializer for games"""

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
        )
