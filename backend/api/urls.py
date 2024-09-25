from django.urls import path
from . import views
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('register/',views.register),
    path('api/login',TokenObtainPairView.as_view(),name='token_obtain_pair'),
    path('api/login/refresh',TokenRefreshView.as_view(),name='token_refresh')
]
