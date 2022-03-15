from django.urls import path


from . import views

urlpatterns = [
    path('', views.auth),
    path('registration/', views.reg),
    path('user/<int:id>/delete/<int:prod_id>/', views.delete),
    path('user/<int:id>/load/<int:prod_id>/', views.load),
    path('user/<int:id>/products/', views.prod),
    path('user/<int:id>/calc/', views.calc),

]