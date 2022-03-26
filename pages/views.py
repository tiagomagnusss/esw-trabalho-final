from django.views.generic import TemplateView

class HomePageView(TemplateView):
    template_name = "home.html"

class ProductListView(TemplateView):
    template_name = "products/index.html"