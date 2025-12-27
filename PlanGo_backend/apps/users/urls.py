from django.urls import path
from apps.users.views import RegisterView, LoginWithGoogleView, LoginWithEmailView, get_userId_by_userUid, create_participant, get_participants_by_destination, get_user_by_id

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login-with-google/', LoginWithGoogleView.as_view(), name='login-with-google'),
    path('login-with-email/', LoginWithEmailView.as_view(), name='login-with-email'),
    path('user/get_id/', get_userId_by_userUid, name='get_userId_by_userUid'),
    path('<int:user_id>/', get_user_by_id, name='get_user_by_id'),
    
    # PARTICIPANT
    path('participant/create/', create_participant, name='create_participant'),
    path('participants/by_destination/<int:destination_id>', get_participants_by_destination, name="get_participants_by_destination"),
]