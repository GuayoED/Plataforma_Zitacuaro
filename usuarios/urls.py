from django.urls import path

from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
    path('login_user', views.login_user, name='login'),
    path('logout_user', views.logout_user, name='logout'),
    path('register_user', views.register_user, name='register_user'),
    path('register_escuela', views.register_escuela, name='register_escuela'),

    #Urls para el cambio de contraseña
    path('reset_password/', auth_views.PasswordResetView.as_view(template_name="authenticate/password_reset_form.html"), name="reset_password"),
    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(template_name="authenticate/password_reset_done.html"), name="password_reset_done"),
    path('rese/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name="authenticate/password_reset.html"), name="password_reset_confirm"),
    #path('reset/<uidb64>/set-password/', auth_views.PasswordChangeView.as_view(), name="password_change"),
    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(template_name="authenticate/password_reset_complete.html"), name="password_reset_complete"),
]