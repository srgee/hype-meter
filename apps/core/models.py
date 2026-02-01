from django.db import models

class TimeStampedModel(models.Model):
    '''
    Abstract base class that provides self-updating tracking fields for record creation and modification.
    '''
    created_at = models.DateTimeField(
        'Record creation date',
        auto_now_add=True,
        db_index=True,
    )
    updated_at = models.DateTimeField(
        'Last modification',
        auto_now_add=True,
    )

    class Meta:
        abstract = True
        ordering = ['-created_at']