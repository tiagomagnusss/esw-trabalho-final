from datetime import timezone
from django.http import Http404, HttpResponseRedirect
from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.forms import ModelForm, TextInput, NumberInput, HiddenInput, DateTimeInput
from django.db.models import Q
from django.contrib.auth.models import User
from django.urls import reverse
from pages.models import Product, Trade, Report


class HomePageView(TemplateView):
    template_name = "home.html"

class AccountsPageView(ListView):
    model = User
    paginate_by = 10
    template_name = "account/index.html"

    def post(self, request, *args, **kwargs):
        data = request.POST
        id = data.get("user_id")
        action = data.get("delete")

        self.object = User.objects.get(id=id)
        if action == "delete":
            self.object.delete()

        return HttpResponseRedirect(request.path_info)

    def get_context_data(self, **kwargs):
        context = super(AccountsPageView, self).get_context_data(**kwargs)
        user = User.objects.all().order_by('username')

        search = self.request.GET.get('search')

        if search:
            user = user.filter(Q(username__icontains=search) | Q(email__icontains=search) | Q(first_name__icontains=search) | Q(last_name__icontains=search))

        paginator = Paginator(user, self.paginate_by)
        page = self.request.GET.get('page')

        try:
            user = paginator.page(page)
        except PageNotAnInteger:
            user = paginator.page(1)
        except EmptyPage:
            user = paginator.page(paginator.num_pages)

        context['users'] = user
        return context

class AccountDetailView(DetailView):
    template_name = "account/account.html"
    model = User

    def post(self, request, *args, **kwargs):
        self.object = User.objects.get(id=kwargs.get('pk'))

        data = request.POST
        action = data.get("delete")
        if action == "delete":
            self.object.delete()

        return HttpResponseRedirect('/')

class ProductListView(ListView):
    paginate_by = 10
    model = Product
    template_name = "products/index.html"

    def get_context_data(self, **kwargs):
        context = super(ProductListView, self).get_context_data(**kwargs)
        product = Product.objects.all().filter(sold=False).order_by('-created_at')

        search = self.request.GET.get('search')
        favorites = self.request.GET.get('favorites')
        own_products = self.request.GET.get('own_products')

        if search:
            product = product.filter(title__icontains=search)
        if favorites == "true":
            product = product.filter(liked_by=self.request.user)
        if own_products == "true":
            product = product.filter(original_owner=self.request.user)


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

    def post(self, request, *args, **kwargs):
        try:
            p = Product.objects.get(original_owner=self.request.user, title=request.POST.get("title"))
            return HttpResponseRedirect(reverse('pages:productupdate', kwargs={'pk': p.id}))
        except Product.DoesNotExist:
            return super().post(request, *args, **kwargs)


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


class ProductSellView(DetailView):
    model = Trade
    template_name = 'products/sell.html'

    def get(self, request, *args, **kwargs):
        self.object = Product.objects.get(id=kwargs.get('pk'))

        if self.object is None:
            raise Http404("Product does not exist")

        context = self.get_context_data(object=self.object)

        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        product = Product.objects.get(id=kwargs.get('pk'))

        # Mark the product as sold in the Product table!
        product.sold = True
        product.save()

        # Fetch data from the form
        data = request.POST
        buyer_email = data.get("buyer_email")
        observation = data.get("observation")

        # Create the receipt
        receipt = Trade(seller=request.user, product=product, buyer_email=buyer_email, observation=observation)
        receipt.save()

        return HttpResponseRedirect(reverse('pages:products'))


class TradeListView(ListView):
    paginate_by = 10
    model = Product
    template_name = "trades/index.html"

    def get_context_data(self, **kwargs):
        context = super(TradeListView, self).get_context_data(**kwargs)
        trade = Trade.objects.all().filter(seller=self.request.user)

        paginator = Paginator(trade, self.paginate_by)
        page = self.request.GET.get('page')

        try:
            trades = paginator.page(page)
        except PageNotAnInteger:
            trades = paginator.page(1)
        except EmptyPage:
            trades = paginator.page(paginator.num_pages)

        context['trades'] = trades
        return context

class ReportListView(ListView):
    paginate_by = 10
    model = Report
    template_name = "reports/index.html"

    def get_context_data(self, **kwargs):
        context = super(ReportListView, self).get_context_data(**kwargs)

        if self.request.user.is_staff:
            report = Report.objects.all()
        else:
            report = Report.objects.all().filter(reporter=self.request.user)

        report = report.order_by('-created_at')
        paginator = Paginator(report, self.paginate_by)
        page = self.request.GET.get('page')

        try:
            reports = paginator.page(page)
        except PageNotAnInteger:
            reports = paginator.page(1)
        except EmptyPage:
            reports = paginator.page(paginator.num_pages)

        context['reports'] = reports
        return context

class ReportForm(ModelForm):
    class Meta:
        model = Report
        fields = ('description',)
        widgets = {
            'description': TextInput(attrs={'class': 'form-control'})
        }
class ReportCreateView(CreateView):
    model = Report
    form_class = ReportForm
    template_name = 'reports/create.html'

    def form_valid(self, form):
        form.instance.reporter = self.request.user
        form.instance.product_id = self.kwargs.get('pk')
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('pages:reportdetail', kwargs={'pk': self.object.id})

    def get_context_data(self, **kwargs):
        context = super(ReportCreateView, self).get_context_data(**kwargs)
        product = Product.objects.get(id=self.kwargs.get('pk'))
        context['product'] = product
        return context

class ReportDetailView(DetailView):
    model = Report
    template_name = 'reports/report.html'

    def get_context_data(self, **kwargs):
        context = super(ReportDetailView, self).get_context_data(**kwargs)
        report = Report.objects.get(id=self.kwargs.get('pk'))
        product = Product.objects.get(id=report.product_id)
        context['report'] = report
        context['product'] = product
        return context

    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            report = Report.objects.get(id=self.kwargs.get('pk'))
            report.resolved = True
            report.save()
            report = Report.objects.get(id=kwargs.get('pk'))

            # set resolved with timestamp
            report.resolved = True
            report.save()

            product = Product.objects.get(id=report.product_id)
            # delete the product
            product.delete()

            return HttpResponseRedirect(reverse('pages:products'))
        else:
            return HttpResponseRedirect(reverse('pages:login'))