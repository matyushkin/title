from django.db import models


class Title(models.Model):
    text = models.CharField(max_length=256)
    timestamp = models.DateTimeField(auto_now_add=True)
    value = models.DecimalField(
        max_digits=3,
        decimal_places=1)
    group_id = models.PositiveIntegerField()

    class Meta:
        ordering = ['timestamp']