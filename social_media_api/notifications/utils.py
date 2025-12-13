from django.contrib.contenttypes.models import ContentType
from .models import Notification


def create_notification(recipient, actor, verb, target=None):
    content_type = None
    object_id = None

    if target:
        content_type = ContentType.objects.get_for_model(target)
        object_id = target.id

    return Notification.objects.create(
        recipient=recipient,
        actor=actor,
        verb=verb,
        content_type=content_type,
        object_id=object_id,
    )


def create_notification_for_like(actor, recipient, post):
    if actor == recipient:
        return None

    return create_notification(
        recipient=recipient,
        actor=actor,
        verb="liked your post",
        target=post,
    )
