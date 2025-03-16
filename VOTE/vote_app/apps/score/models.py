from django.db import models

class Session(models.Model):
  session_id = models.CharField(max_length=3)
  title = models.CharField(max_length=100)
  speaker = models.CharField(max_length=50)

  def __str__(self):
    return f"{self.session_id} - {self.title} ({self.speaker})"

  class Meta:
    constraints = [
      models.UniqueConstraint(
        fields=['session_id'],
        name='unique_session'
      ),
    ]
