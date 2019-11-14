from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('/<api_token>/<refid>', views.authenticate, name='authenticate'),
]
