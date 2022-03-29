from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

app_name = "pages"

urlpatterns = [
    path("", views.HomePageView.as_view(), name = 'home'),
    path("products/", views.ProductListView.as_view(), name = 'products'),
    path('products/<int:pk>/', views.ProductDetailView.as_view(), name='productdetail'),
    path('products/add/', views.ProductCreateView.as_view(), name='productcreate'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)