from django.urls import path

from . import views

urlpatterns = [
    path('<int:user_id>/<int:api_token>/<int:refid>', views.index, name='index'),
    path('<int:user_id>/<int:api_token>/<int:refid>/validate',
         views.authenticate, name='authenticate'),
]
