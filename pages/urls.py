from django.urls import path

from . import views

app_name = "pages"

urlpatterns = [
    path("", views.HomePageView.as_view(), name = 'home'),
    path("products/", views.ProductListView.as_view(), name = 'products'),
]