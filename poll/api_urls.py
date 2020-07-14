from poll.views import *

from django.urls import path, include

from rest_framework.routers import DefaultRouter, SimpleRouter

# router = DefaultRouter()
# router.register('poll',PollViewSet)

# poll_list_view = PollViewSet.as_view({
#     "get": "list",
#     "post": "create"
# })    


urlpatterns = [
    # path('poll/', poll),
    # path('poll/<int:id>/', poll_detail)
    # path('poll/', PollAPIView.as_view()),
    # path('poll/<int:id>/', PollDetailView.as_view()),
    path('generic/poll/', PollGenericView.as_view(), name='generic-poll'),
    path('generic/poll/<int:id>/', PollGenericView.as_view()),
    # path('viewset/poll/', poll_list_view),
    # path('poll/', include(router.urls)),
]