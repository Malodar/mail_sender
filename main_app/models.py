from django.db import models
# Create your models here.


class Event(models.Model):
    day = models.DateField('Day of the event')
    time = models.TimeField('Time of the event')
    file_csv = models.FileField(upload_to='upload')

    class Meta:
        verbose_name = 'Scheduling'
        verbose_name_plural = 'Scheduling'

    def __str__(self):
        return str(f'{self.day} : {self.time}')
