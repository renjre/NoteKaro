
from django.urls import path
from note.views import NoteView, NoteDetailsView, RegisterView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('user-registeration/', RegisterView.as_view(), name='create_note'),
    path('my-notes/', NoteView.as_view(), name='create_note'),
    path('my-notes/<int:pk>/', NoteDetailsView.as_view(), name='created_note'),
]