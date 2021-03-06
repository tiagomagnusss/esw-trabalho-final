from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

app_name = "pages"

urlpatterns = [
    path("", views.HomePageView.as_view(), name='home'),
    path("accounts/", views.AccountsPageView.as_view(), name='accounts'),
    path("accounts/<int:pk>/", views.AccountDetailView.as_view(), name='accountdetail'),
    path("products/", views.ProductListView.as_view(), name='products'),
    path('products/<int:pk>/', views.ProductDetailView.as_view(), name='productdetail'),
    path('products/add/', views.ProductCreateView.as_view(), name='productcreate'),
    path('products/update/<int:pk>/', views.ProductUpdateView.as_view(), name='productupdate'),
    path('products/delete/<int:pk>/', views.ProductDeleteView.as_view(), name='productdelete'),
    path('products/sell/<int:pk>/', views.ProductSellView.as_view(), name='productsell'),
    path("trades/", views.TradeListView.as_view(), name='trades'),
    path("reports/", views.ReportListView.as_view(), name='reports'),
    path("reports/add?pk=<int:pk>", views.ReportCreateView.as_view(), name='reportcreate'),
    path("reports/<int:pk>/", views.ReportDetailView.as_view(), name='reportdetail'),
    path("reports/<int:pk>/", views.ReportDetailView.as_view(), name='reportaccept'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
