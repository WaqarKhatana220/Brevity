from apps.blog.models import Author
from apps.subscribers.admin import Subscribers
from rest_framework.exceptions import ValidationError, PermissionDenied


class SubscriptionHandler:
    def validate_subscription(self, author_id, user):
        try:
            author = Author.objects.get(id=author_id)
            if author.is_subscribed_by(user):
                raise ValidationError("User is already subscribed to this author.")
            if user == author.user:
                raise PermissionDenied("Author cannot subscribe to self.")
        except Author.DoesNotExist:
            raise Author.DoesNotExist("Author does not exist.")
        return author

    def validate_unsubscription(self, author_id, user):
        try:
            author = Author.objects.get(id=author_id)
            if not author.is_subscribed_by(user):
                raise ValidationError("User is not subscribed to this author.")
            if user == author.user:
                raise PermissionDenied("Invalid action.")
        except Author.DoesNotExist:
            raise Author.DoesNotExist("Author does not exist.")
        return author

    def subscribe_author(self, author, user):
        return Subscribers.objects.create(subscriber=user, author=author)

    def unsubscribe_author(self, author, user):
        return Subscribers.objects.filter(subscriber=user, author=author).delete()
