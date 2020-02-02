from api import views
from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework_simplejwt import views as jwt_views


staff_url = [
     path('staff/signup/', views.AccountSignup.as_view(),
         kwargs={'is_staff': True}, name='staff_signup'),
    path('staff/login/', views.AccountLogin.as_view(), name='staff_login'),
    path('staff/teams/', views.TeamsList.as_view(), name='teams'),
    path('staff/fixtures/', views.FixturesList.as_view(), name='fixtures'),
    path('staff/fixtures/<str:link_address>/', views.FixturesList.as_view(), name='edit_fixtures'),
    ]

user_url = [
     path('signup/', views.AccountSignup.as_view(),
         kwargs={'is_staff': False}, name='user_signup'),
     path('login/', views.AccountLogin.as_view(), name='user_login'),
     path('teams/', views.teams_list, name='user_teams'),
     path('fixtures/<str:fixture_type>/', views.fixtures, name='user_fixtures'),
]
urlpatterns = [
     *staff_url,
     *user_url,
    path('token/', jwt_views.TokenObtainPairView.as_view(),
         name='token_obtain_pair'),
    path('token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
    
    path('home/', views.HomeView.as_view(), name='home'),
#     path('login/', views.AccountLogin.as_view(), name='login'),

]

urlpatterns = format_suffix_patterns(urlpatterns)
