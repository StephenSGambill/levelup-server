from django.db import models


class Event(models.Model):
    # Model fields
    description = models.CharField(max_length=50)
    date = models.DateField()
    time = models.TimeField()

    # Field to establish a many-to-one relationship with the "Gamer" model
    # on_delete=models.CASCADE specifies that if the related Gamer is deleted,
    # all related Events will be deleted as well
    organizer = models.ForeignKey(
        "Gamer",
        on_delete=models.CASCADE,
        related_name="events",
    )

    # NB: The 'related_name' parameter is used to define the reverse relation from the related model back to the model
    # that contains the foreign key or the many-to-many relationship.

    # Field to establish a many-to-many relationship with the "Gamer" model
    # This allows multiple gamers to attend the event
    attendees = models.ManyToManyField("Gamer", related_name="attended_events")

    # Field to establish a one-to-many relationship with the "Game" model
    # on_delete=models.CASCADE specifies that if the related Game is deleted,
    # all related Events will be deleted as well
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
