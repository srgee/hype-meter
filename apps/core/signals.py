from django.core.signals import request_finished
from django.dispatch import receiver
from .context_vars import request_id_var

@receiver(request_finished)
def clear_logging_context(sender, **kwargs):
    request_id_var.reset(None)