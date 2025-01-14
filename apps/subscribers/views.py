import logging
from apps.blog.models import Author
from .models import Subscribers
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_500_INTERNAL_SERVER_ERROR,
    HTTP_404_NOT_FOUND,
    HTTP_200_OK,
    HTTP_403_FORBIDDEN,
    HTTP_500_INTERNAL_SERVER_ERROR,
)
from rest_framework.generics import ListAPIView
from .serializers import SubscribersSerializer, SubscribedAuthorsSerializer
from django_filters.rest_framework import DjangoFilterBackend
from .filters import SubscribersListingFilter
from .subscription_handler import SubscriptionHandler
from rest_framework.exceptions import ValidationError, PermissionDenied

logger = logging.getLogger("django")
# Create your views here.


class SubscribeAuthorView(SubscriptionHandler, APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, author_id, *args, **kwargs):
        try:
            author = self.validate_subscription(author_id, request.user)
            self.subscribe_author(author, request.user)
            return Response(
                {"message": "You have successfully subscribed to this author."},
                status=HTTP_200_OK,
            )
        except Author.DoesNotExist as e:
            logger.error(f"Author with id {author_id} does not exist.")
            return Response({"message": "Author does not exist"}, status=HTTP_404_NOT_FOUND)
        except PermissionDenied as e:
            logger.error("Author cannot subscribe to self.")
            return Response({"message": "Can not subscribe to self"}, status=HTTP_400_BAD_REQUEST)
        except ValidationError as e:
            logger.error(f"User is already subscribed to the author with id {author_id}")
            return Response({"message": "User is already subscribed to this author"}, status=HTTP_403_FORBIDDEN)
        except Exception as e:
            logger.error(
                f"An unexpected error occurred while subscribing to author: {e}"
            )
            return Response(
                {"message": "An error occurred. Please try again later."},
                status=HTTP_500_INTERNAL_SERVER_ERROR,
            )


class UnSubscribeAuthorView(SubscriptionHandler, APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, author_id, *args, **kwargs):
        try:
            author = self.validate_unsubscription(author_id, request.user)
            self.unsubscribe_author(author, request.user)
            return Response(
                {"message": "You have successfully unsubscribed from this author."},
                status=HTTP_200_OK,
            )
        except Author.DoesNotExist as e:
            logger.error(f"Author with id {author_id} does not exist.")
            return Response({"message": "Author does not exist"}, status=HTTP_404_NOT_FOUND)
        except (ValidationError, PermissionDenied) as e:
            logger.error(f"An error occurred while unsubscribing from author: {e}")
            return Response({"message": "Invalid action"}, status=HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error(
                f"An unexpected error occurred while unsubscribing from author: {e}"
            )
            return Response(
                {"message": "An error occurred. Please try again later."},
                status=HTTP_500_INTERNAL_SERVER_ERROR,
            )


class SubscriptionStatus(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, author_id, *args, **kwargs):
        try:
            author = Author.objects.get(id=author_id)
            user = request.user
            is_subscribed = user.is_subscribed_to(author)
            return Response(
                {"author_id": author_id, "is_subscribed": str(is_subscribed)},
                status=HTTP_200_OK,
            )
        except Author.DoesNotExist:
            logger.error(f"Author with id {author_id} does not exist.")
            return Response(
                {"message": "Author does not exist."}, status=HTTP_404_NOT_FOUND
            )
        except Exception as e:
            logger.error(
                f"An unexpected error occurred while checking subscription status: {e}"
            )
            return Response(
                {"message": "An error occurred. Please try again later."},
                status=HTTP_500_INTERNAL_SERVER_ERROR,
            )


class SubscribersListView(ListAPIView):
    queryset = Subscribers.objects.all()
    serializer_class = SubscribersSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = SubscribersListingFilter
    permission_classes = [IsAuthenticated]


class SubscribedAuthorsView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = SubscribedAuthorsSerializer

    def get_queryset(self):
        user = self.request.user
        return Subscribers.objects.filter(user=user)
