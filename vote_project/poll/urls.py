from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('createPoll', views.createPoll, name='createPoll'),
    path('votePage/<poll_id>', views.votePage, name='votePage'),
    path('result/<poll_id>', views.result, name='result'),
    path('login', views.login_user, name='login'),
    path('signup', views.register, name='signup'),
    path('logout', views.logout_user, name='logout'),
    path('delete/<int:poll_id>/', views.delete_poll, name='delete_poll'),

]