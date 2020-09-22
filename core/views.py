from django.conf import settings
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import TemplateView, ListView, DetailView, View
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import ReviewForm, CheckoutForm, RefundForm, CouponForm, ContactForm, NewsletterForm
from django.utils import timezone
from django.db.models import Q
from django.urls import reverse_lazy, reverse
from django.template.loader import render_to_string
from django.core.mail import send_mail, EmailMessage
# from .filters import ItemFilter
from django.core.paginator import Paginator


from .models import (
    Item,
    Wishlist,
    Reviews,
    OrderItem,
    Order,
    Address,
    Payment,
    Coupon,
    Refund,
    UserProfile,
    Category,
    HomepageBanner,
    HomesideBanner,
    ShoptopBanner,
    ShopbottomBanner,

    Contact,
    Slider,
    Newsletter,
    About
)


# Create your views here.
class DetailView(DetailView):
    model = Item
    context_object_name = 'product'
    template_name = "single-product.html"

    def post(self, request, *args, **kwargs):
        form = ReviewForm(self.request.POST)

        if form.is_valid():
            review = form.cleaned_data.get('review')
            user = self.request.user
            item = self.get_object()

            review = Reviews(
                user=user,
                item=item,
                review=review
            )
            review.save()
            messages.success(
                self.request, 'Yay, you are amazing for the review')
            return redirect('core:details', slug=item.slug)
        messages.error(self.request, 'Oh no, you didn\'t any review')
        return redirect('core:details', slug=self.get_object().slug)

    def get_object(self, **kwargs):
        qs = super().get_object(**kwargs)
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        trip = get_object_or_404(Item, slug=self.get_object().slug)
        trip_related = trip.tags.similar_objects()
        context.update({
            'form': ReviewForm(),
            "trip_related": trip_related

        })
        return context


class ShopView(ListView):
    model = Item
    context_object_name = 'product'
    paginate_by = 24
    template_name = "shop.html"

    def get_queryset(self):
        qs = Item.objects.order_by('-pub_date')
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(
            {
                'category_list': Category.objects.all(),
                "shoptop": ShoptopBanner.objects.order_by('-date')[:2],
                "shopside": ShopbottomBanner.objects.order_by('-date')[:1]
            })
        return context


class AboutView(TemplateView):
    template_name = "about.html"


class HomeView(TemplateView):
    template_name = "index.html"

    def post(self, request, *args, **kwargs):
        newsletter = NewsletterForm(self.request.POST)

        if newsletter.is_valid():
            email = newsletter.cleaned_data.get('email')
            existing = Newsletter.objects.filter(email=email).count()

            if existing == 0:
                news = Newsletter(
                    email=email
                )
                news.save()
                messages.success(
                    self.request, 'You have signup for the newsletter')
                return redirect('core:home')
            else:
                messages.success(
                    self.request, 'You have already used this email')
                return redirect('core:home')
        messages.error(
            self.request, 'You haven\'t signed up for the newsletter')
        return redirect('core:home')

    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)
        context.update({

            'newsletter': NewsletterForm()
        })
        return context


class ContactView(TemplateView):
    template_name = "contact.html"

    def post(self, request, *args, **kwargs):
        form = ContactForm(self.request.POST or None)

        if form.is_valid():
            name = form.cleaned_data.get('name')
            email = form.cleaned_data.get('email')
            subject = form.cleaned_data.get('subject')
            message = form.cleaned_data.get('message')

            contact = Contact(
                name=name,
                message=message,
                subject=subject,
                email=email
            )

            context = {
                "name": name,
                "subject": subject,
                "message": message
            }
            contact.save()
            template = render_to_string('contact_template.html', context)
            mail = EmailMessage(
                'We have a new mail',
                template,
                "mail@stroyalstoi.com",
                ['mail@stroyalstoi.com']

            )
            mail.fail_silently = False
            mail.send()

            return redirect('core:contact-success')

    def get_context_data(self, **kwargs):
        context = super(ContactView, self).get_context_data(**kwargs)
        context.update({
            'form': ContactForm()
        })
        return context


class ContactSuccessView(TemplateView):
    template_name = "contact-success.html"


@login_required
def wishlist(request, slug):
    item = get_object_or_404(Item, slug=slug)
    wish_qs = Wishlist.objects.filter(user=request.user, item=item)
    if wish_qs.exists():
        wish_qs[0].delete()
        messages.error(request, "You have removed an item to your wishlist")
        return redirect('core:shop')
    Wishlist.objects.create(user=request.user, item=item)
    messages.success(request, "You have added an item to your wishlist")
    return redirect('core:shop')


@login_required
def wishlist_product(request, slug):
    item = get_object_or_404(Item, slug=slug)
    wish_qs = Wishlist.objects.filter(user=request.user, item=item)
    if wish_qs.exists():
        wish_qs[0].delete()
        messages.error(request, "You have removed an item to your wishlist")
        return redirect('core:details', slug=slug)
    Wishlist.objects.create(user=request.user, item=item)
    messages.success(request, "You have added an item to your wishlist")
    return redirect('core:details', slug=slug)


@login_required
def wishlist_home(request, slug):
    item = get_object_or_404(Item, slug=slug)
    wish_qs = Wishlist.objects.filter(user=request.user, item=item)
    if wish_qs.exists():
        wish_qs[0].delete()
        messages.error(request, "You have removed an item to your wishlist")
        return redirect('core:home')
    Wishlist.objects.create(user=request.user, item=item)
    messages.success(request, "You have added an item to your wishlist")
    return redirect('core:home')


@login_required
def add_to_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_item, created = OrderItem.objects.get_or_create(
        item=item,
        user=request.user,
        ordered=False
    )
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in the order
        if order.items.filter(item__slug=item.slug).exists():
            order_item.quantity += 1
            order_item.save()
            messages.info(request, "This item quantity was updated.")
            return redirect("core:cart")
        else:
            order.items.add(order_item)
            messages.info(request, "This item was added to your cart.")
            return redirect("core:cart")
    else:
        ordered_date = timezone.now()
        order = Order.objects.create(
            user=request.user, ordered_date=ordered_date)
        order.items.add(order_item)
        messages.info(request, "This item was added to your cart.")
        return redirect("core:cart")


@login_required
def remove_from_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_qs = Order.objects.filter(
        user=request.user,
        ordered=False
    )
    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in the order
        if order.items.filter(item__slug=item.slug).exists():
            order_item = OrderItem.objects.filter(
                item=item,
                user=request.user,
                ordered=False
            )[0]
            order.items.remove(order_item)
            order_item.delete()
            messages.info(request, "This item was removed from your cart.")
            return redirect("core:cart")
        else:
            messages.info(request, "This item was not in your cart")
            return redirect("core:details", slug=slug)
    else:
        messages.info(request, "You do not have an active order")
        return redirect("core:details", slug=slug)


@login_required
def remove_single_item_from_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_qs = Order.objects.filter(
        user=request.user,
        ordered=False
    )
    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in the order
        if order.items.filter(item__slug=item.slug).exists():
            order_item = OrderItem.objects.filter(
                item=item,
                user=request.user,
                ordered=False
            )[0]
            if order_item.quantity > 1:
                order_item.quantity -= 1
                order_item.save()
            else:
                order.items.remove(order_item)
            messages.info(request, "This item quantity was updated.")
            return redirect("core:cart")
        else:
            messages.info(request, "This item was not in your cart")
            return redirect("core:details", slug=slug)
    else:
        messages.info(request, "You do not have an active order")
        return redirect("core:details", slug=slug)


class CheckoutView(LoginRequiredMixin, TemplateView):
    template_name = 'checkout.html'

    def get(self, *args, **kwargs):
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            form = CheckoutForm()

            context = {
                'form': form,
                'couponform': CouponForm(),
                'order': order,
                'DISPLAY_COUPON_FORM': True
            }
            return render(self.request, "checkout.html", context)
        except ObjectDoesNotExist:
            messages.info(self.request, "You do not have an active order")
            return redirect("core:checkout")

    def get_context_data(self, **kwargs):
        context = super(CheckoutView, self).get_context_data(**kwargs)
        context.update({
            'form': CheckoutForm()
        })
        return context

    def post(self, request, *args, **kwargs):
        form = CheckoutForm(self.request.POST or None)
        order = Order.objects.get(user=self.request.user, ordered=False)

        if form.is_valid():
            user = self.request.user
            address = form.cleaned_data.get('address')
            country = form.cleaned_data.get('country')
            zip = form.cleaned_data.get('zip')
            state = form.cleaned_data.get('state')
            phone = form.cleaned_data.get('phone')

            checkout = Address(
                user=user,
                address=address,
                country=country,
                state=state,
                zip=zip,
                phone=phone,

            )
            checkout.save()
            order.address = checkout
            order.save()
            amount = order.get_total()
            user = self.request.user
            email = self.request.user.email
            name = self.request.user.first_name
            name_2 = self.request.user.last_name
            number = order.address.phone
            address = order.address.address
            country = order.address.country
            state = order.address.state

            context = {
                'order': order,
                'amount': amount,
                'email': email,
                'name': name,
                'user': user,

                "name_2": name_2,
                "address": address,
                "country": country,
                'state': state,
                'number': number
            }
            template = render_to_string('email_template.html', context)
            sale = EmailMessage(
                'Thank you for your order!!',
                template,
                "mail@stroyalstoi.com",
                [email]

            )
            sale.fail_silently = False
            sale.send()

            template = render_to_string('sale_template.html', context)
            sale = EmailMessage(
                'We have received an order!!',
                template,
                "mail@stroyalstoi.com",
                ['admin@stroyalstoi.com']

            )
            sale.fail_silently = False
            sale.send()
            order.ordered = True
            order_items = order.items.all()

            order_items.update(ordered=True)
            for item in order_items:
                item.save()
            order.save()
    # send email to user

            return redirect('core:payment')
        messages.error(self.request, 'You didn\'t enter any address')
        return redirect('core:checkout')


class CartView(LoginRequiredMixin, TemplateView):
    template_name = 'cart.html'

    def get(self, *args, **kwargs):
        try:
            shoptop = ShoptopBanner.objects.all()[:2]
            order = Order.objects.get(user=self.request.user, ordered=False)
            context = {
                'object': order,

            }
            return render(self.request, 'cart.html', context)
        except ObjectDoesNotExist:
            messages.warning(self.request, "You do not have an active order")
            return redirect("/")


class PaystackView(LoginRequiredMixin, TemplateView):
    template_name = "confirmation.html"


class ConfirmView(TemplateView):
    template_name = 'payment-confirmation.html'

    def get_context_data(self, **kwargs):
        context = super(ConfirmView, self).get_context_data(**kwargs)

        context.update({
            'order': Order.objects.filter(user=self.request.user, ordered=True)
        })
        return context


class FailedView(TemplateView):
    template_name = 'payment-failed.html'


class SearchListView(ListView):
    model = Item
    context_object_name = 'queryset'
    paginate_by = 18
    template_name = "search.html"

    def get_context_data(self, **kwargs):
        context = super(SearchListView, self).get_context_data(**kwargs)
        query = self.request.GET.get('q')
        context.update({
            'category_list': Category.objects.all(),
            'query': query,
                   "shoptop": ShoptopBanner.objects.order_by('-date')[:2],
                "shopside": ShopbottomBanner.objects.order_by('-date')[:1]
        })
        return context

    def get_queryset(self):
        query = self.request.GET.get('q', None)
        if query is not None:
            search = Q(title__icontains=query) | Q(
                description__icontains=query)
            queryset = Item.objects.filter(search).distinct()[:20]
            return queryset
        return render(self.request, 'search.html')


def CategoryView(request, slug):
    instance = Item.objects.all()
    categories = Category.objects.all()

    if slug:
        category = get_object_or_404(Category, slug=slug)
        instance_list = instance.filter(category=category)
        paginator = Paginator(instance_list, 18)
        page = request.GET.get('page')
        instance = paginator.get_page(page)
        shoptop = ShoptopBanner.objects.order_by('-date')[:2]
        shopside = ShopbottomBanner.objects.order_by('-date')[:1]
    content = {
        'categories': categories,
        'instance': instance,
        "instance_list": instance_list,
        'category': category,
        "shoptop": shoptop,
        "shopside": shopside,



    }
    return render(request, 'category.html', content)


def handler404(request, exception):
    return render(request, '404.html')