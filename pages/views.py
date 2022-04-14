from django.contrib.auth.models import User
from django.http import Http404, HttpResponseRedirect

from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.forms import ModelForm, TextInput, NumberInput
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
        search = self.request.GET.get('search')
        favorites = self.request.GET.get('favorites')

        if search:
            product = product.filter(title__icontains=search)
        if favorites == "true":
            product = product.filter(liked_by=self.request.user)

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
    model = Product

    def post(self, request, *args, **kwargs):
        self.object = Product.objects.get(id=kwargs.get('pk'))

        data = request.POST
        action = data.get("like")
        if action == "like":
            self.object.liked_by.add(request.user)
        elif action == "dislike":
            self.object.liked_by.remove(request.user)

        return HttpResponseRedirect(request.path_info)

    def get(self, request, *args, **kwargs):
        self.object = Product.objects.get(id=kwargs.get('pk'))

        if self.object is None:
            raise Http404("Product does not exist")

        is_already_liked = False
        # Check if user already likes this product or not.
        if request.user.is_authenticated:
            register = Product.objects.filter(id=kwargs.get('pk'), liked_by=request.user)
            if register:
                is_already_liked = True

        context = self.get_context_data(object=self.object, owner=self.object.original_owner, is_already_liked=is_already_liked)

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


class ProductUpdateView(UpdateView):
    model = Product
    form_class = ProductForm

    template_name = 'products/update.html'

    def form_valid(self, form):
        form.instance.original_owner = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('pages:productdetail', kwargs={'pk': self.object.id})


class ProductDeleteView(DeleteView):
    template_name = 'products/delete.html'
    model = Product

    def get(self, request, *args, **kwargs):
        self.object = Product.objects.get(id=kwargs.get('pk'))

        if self.object is None:
            raise Http404("Product does not exist")

        context = self.get_context_data(object=self.object)

        return self.render_to_response(context)

    def get_success_url(self):
        return reverse('pages:products')

