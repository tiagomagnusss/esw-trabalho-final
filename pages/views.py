from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.forms import ModelForm, TextInput, NumberInput, CheckboxInput
from django.urls import reverse
from pages.models import Product

class HomePageView(TemplateView):
    template_name = "home.html"

class ProductListView(ListView):
    paginate_by = 10
    model = Product
    template_name = "products/index.html"

    def get_context_data(self, **kwargs):
        context = super(ProductListView, self).get_context_data(**kwargs)
        product = Product.objects.all().order_by('created_at')
        paginator = Paginator(product, self.paginate_by)
        page = self.request.GET.get('page')

        try:
            products = paginator.page(page)
        except PageNotAnInteger:
            products = paginator.page(1)
        except EmptyPage:
            products = paginator.page(paginator.num_pages)

        context['products'] = products
        return context

class ProductDetailView(DetailView):
    template_name = "products/product.html"

    def get (self,request,*args,**kwargs):
        self.object = Product.objects.get(id=kwargs.get('pk'))

        if self.object is None:
            raise Http404("Product does not exist")

        context = self.get_context_data(object=self.object, owner=self.object.original_owner)
        return self.render_to_response(context)

class ProductForm(ModelForm):
    class Meta:
        model = Product
        # fields = ['title', 'description', 'price']
        fields = ('title', 'description', 'price', 'image')
        widgets = {
            'title': TextInput(attrs={'class': 'form-control'}),
            'description': TextInput(attrs={'class': 'form-control'}),
            'price': NumberInput(attrs={'class': 'form-control'}),
        }


class ProductCreateView(CreateView):
    model = Product
    form_class = ProductForm
    template_name = 'products/create.html'

    def form_valid(self, form):
        form.instance.original_owner = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('pages:productdetail', kwargs={'pk': self.object.id})
