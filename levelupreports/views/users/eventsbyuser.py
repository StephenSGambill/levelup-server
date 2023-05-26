"""Module for generating games by user report"""
from django.shortcuts import render
from django.db import connection
from django.views import View

from levelupreports.views.helpers import dict_fetch_all


class EventsByUser(View):
    def get(self, request):
        with connection.cursor() as db_cursor:
            # TODO: Write a query to get all games along with the gamer first name, last name, and id
            db_cursor.execute(
                """
                SELECT 
                    gamer_id,
                    full_name,
                    event_id,
                    event_date,
                    event_time,
                    game_name
                FROM 
                    EVENTS_BY_USER
                """
            )
            dataset = dict_fetch_all(db_cursor)

            # Take the flat data from

            events_by_gamer = []

            for row in dataset:
                # TODO: Create a dictionary called game that includes
                # the name, description, number_of_players, maker,
                # game_type_id, and skill_level from the row dictionary
                event = {
                    "event_id": row["event_id"],
                    "event_date": row["event_date"],
                    "event_time": row["event_time"],
                    "game_name": row["game_name"],
                }

                # See if the gamer has been added to the games_by_user list already
                gamer_dict = None
                for gamer_event in events_by_gamer:
                    if gamer_event["gamer_id"] == row["gamer_id"]:
                        gamer_dict = gamer_event

                if gamer_dict:
                    # If the user_dict is already in the games_by_user list, append the game to the games list
                    gamer_dict["events"].append(event)
                else:
                    # If the user is not on the games_by_user list, create and add the user to the list
                    events_by_gamer.append(
                        {
                            "gamer_id": row["gamer_id"],
                            "full_name": row["full_name"],
                            "events": [event],
                        }
                    )

        template = "users/list_with_events.html"

        context = {"userevent_list": events_by_gamer}

        return render(request, template, context)
