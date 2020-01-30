from django.urls import path
from api import views
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework_simplejwt import views as jwt_views


urlpatterns = [
    path('token/', jwt_views.TokenObtainPairView.as_view(),
         name='token_obtain_pair'),
    path('token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
    path('signup/', views.AccountSignup.as_view(),
         kwargs={'is_staff': False}, name='user_signup'),
    path('staff/signup/', views.AccountSignup.as_view(),
         kwargs={'is_staff': True}, name='staff_signup'),
    path('fixtures/', views.FixturesList.as_view(), name='fixtures'),
    path('home/', views.HomeView.as_view(), name='home'),
    path('login/', views.AccountLogin.as_view(), name='login'),
    path('teams/', views.TeamsList.as_view(), name='teams'),

]

urlpatterns = format_suffix_patterns(urlpatterns)
