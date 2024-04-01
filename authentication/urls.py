from django.urls import path, include

from authentication.views import (
    LoginUserView,
    RegisterView,
    ProfileView,
    UserView,
    LogoutView,
)

urlpatterns = [
    path("login", LoginUserView.as_view(), name="login_user"),
    path("register", RegisterView.as_view(), name="register_user"),
    path("logout", LogoutView.as_view(), name="logout_user"),
    path(
        "users/",
        include(
            [
                path("me", ProfileView.as_view(), name="profile"),
                path("<str:username>", UserView.as_view(), name="user"),
            ]
        ),
    ),
]
