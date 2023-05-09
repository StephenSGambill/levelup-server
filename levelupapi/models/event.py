from django.db import models


class Event(models.Model):
    description = models.CharField(max_length=50)
    date = models.DateField(auto_now=False, auto_now_add=False)
    time = models.TimeField()
    organizer = models.ForeignKey(
        "Gamer",
        on_delete=models.CASCADE,
        related_name="events",
    )
    attendees = models.ManyToManyField("Gamer", related_name="attended_events")
    game = models.ForeignKey("Game", on_delete=models.CASCADE, related_name="events")

    # Property getter for the "joined" status of the event
    # This property can be accessed as an attribute of an Event object
    @property
    def joined(self):
        return self.__joined

    # Property setter for the "joined" property
    # This allows setting the value of "joined" as an attribute of an Event object
    @joined.setter
    def joined(self, value):
        self.__joined = value
