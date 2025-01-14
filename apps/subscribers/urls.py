from django.urls import path
from .views import SubscribeAuthorView, UnSubscribeAuthorView, SubscriptionStatus, SubscribersListView, SubscribedAuthorsView 

urlpatterns = [
    path('<int:author_id>/subscribe', SubscribeAuthorView.as_view(), name='subscribe_author'),
    path('<int:author_id>/unsubscribe', UnSubscribeAuthorView.as_view(), name='unsubscribe_author'),
    path('<int:author_id>/status', SubscriptionStatus.as_view(), name='subscription_status'),
    path('list/subscribers', SubscribersListView.as_view(), name='list_subscribers'),
    path('list/subscriptions', SubscribedAuthorsView.as_view(), name='list_subscribed_authors')
    
]