from django.contrib.auth import views as auth_views
from django.urls import path

from . import views

urlpatterns = [
    path("", views.task_list, name="task_list"),
    path("add/", views.task_create, name="task_create"),
    path("<int:pk>/edit/", views.task_update, name="task_update"),
    path("<int:pk>/toggle/", views.task_toggle, name="task_toggle"),
    path("<int:pk>/delete/", views.task_delete, name="task_delete"),

    path("register/", views.register, name="register"),
    path(
        "login/",
        auth_views.LoginView.as_view(
            template_name="tasks/login.html", redirect_authenticated_user=True
        ),
        name="login",
    ),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
]
