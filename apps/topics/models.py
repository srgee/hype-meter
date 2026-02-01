from django.db import models

from apps.core.models import TimeStampedModel

class TopicManager(models.Manager):
    '''
    Manager to encapsulate logic for creating or updating topics.
    Ensures that data integrity (like lowercase names) is handled 
    at the persistence layer.
    '''
    def update_hype_data(self, keyword, score, history_data):
        topic, created = self.update_or_create(
            name=keyword.lower().strip(),
            defaults={
                'score': score,
                'history_data': history_data
            }
        )
        return topic

class Topic(TimeStampedModel):
    '''
    Represents a search term and its calculated hype metrics.
    Inherits from TimestampedModel to track creation and updates.
    '''
    name = models.CharField(
        'Keyword',
        max_length=255, 
        unique=True, 
        db_index=True,
        help_text='The normalized search term.'
    )
    score = models.PositiveIntegerField(
        'Hype scoring value',
        default=0,
        help_text='Weighted average score (0-100).'
    )
    history_data = models.JSONField(
        'History data',
        default=dict,
        help_text='Stores the 7-day pulse data for charting.'
    )

    objects = TopicManager()

    class Meta:
        verbose_name = 'Topic'
        verbose_name_plural = 'Topics'
        ordering = ['-score']

    def __str__(self):
        return f'{self.name} ({self.score}/100)'
    
    @property
    def status_label(self):
        '''
        Calculates the status based on defined thresholds.
        '''
        if self.score >= 90:
            return 'VIRAL'
        elif self.score >= 50:
            return 'NEUTRAL'
        else:
            return 'DEAD ZONE'

    def is_stale(self):
        '''
        Determines if the topic data is older than 24 hours.
        '''
        from django.utils import timezone
        from datetime import timedelta
        return timezone.now() > self.updated_at + timedelta(hours=24)