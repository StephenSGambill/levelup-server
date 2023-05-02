from django.db import models


class Event(models.Model):
    description = models.CharField(max_length=50)
    date = models.DateField()
    time = models.TimeField()
    organizer = models.ForeignKey(
        "Gamer",
        on_delete=models.CASCADE,
        related_name="events",
    )
    attendees = models.ManyToManyField("Gamer")
    game = models.ForeignKey("Game", on_delete=models.CASCADE, related_name="events")
