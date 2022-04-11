from django.urls import path

from appRevyakoES.views import Views

urlpatterns = [
    path('', Views.auth),
    path('registration/', Views.reg),
    path('user/<int:id>/delete/<int:prod_id>/', Views.delete),
    path('user/<int:id>/load/<int:prod_id>/', Views.load),
    path('user/<int:id>/products/', Views.prod),
    path('user/<int:id>/calc/', Views.calc),
]