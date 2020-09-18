from django.contrib import admin

from .models import (
    Item,
    OrderItem,
    Order,
    Payment,
    Coupon,
    Refund,
    Address,
    UserProfile,
    Category,
    HomepageBanner,
    HomesideBanner,
    ShoptopBanner,
    ShopbottomBanner,
    Reviews,
    Contact,
    Slider, 
    Author,
    Wishlist,
    Newsletter,
    About,
     CustomUser

)


def make_refund_accepted(modeladmin, request, queryset):
    queryset.update(refund_requested=False, refund_granted=True)


make_refund_accepted.short_description = 'Update orders to refund granted'


class OrderAdmin(admin.ModelAdmin):
    list_display = ['user',
                    'order_id',
                    'ordered',
                    'being_delivered',
                    'received',
                    'refund_requested',
                    'refund_granted',
               
                    'address',
                    'payment',
                    'coupon',

                    ]
    list_display_links = [
        'user',
        'address',

        'payment',
        'coupon'
    ]
    list_filter = ['ordered',
                   'being_delivered',
                   'received',
                   'refund_requested',
                   'refund_granted']
    search_fields = [
        'user__username',
        'ref_code'
    ]
    actions = [make_refund_accepted]


class AddressAdmin(admin.ModelAdmin):
    list_display = [
        'user',
        'address',

        'country',
        'zip',
        'default'
    ]
    list_filter = ['default', 'country']
    search_fields = ['user', 'address','zip']


class ItemAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}


class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}


class OrderItemAdmin(admin.ModelAdmin):
    list_display = [
        'user',
        'order_id',
        'quantity',
        'item',


    ]


class ContactAdmin(admin.ModelAdmin):
    list_display = ['name', 'time', 'subject']


class PaymentAdmin(admin.ModelAdmin):
    list_display = ['reference', 'user', 'amount', "timestamp"]


admin.site.register(Item, ItemAdmin)
admin.site.register(OrderItem, OrderItemAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(Payment, PaymentAdmin)
admin.site.register(Coupon)
admin.site.register(Refund)
admin.site.register(Address, AddressAdmin)
admin.site.register(UserProfile)
admin.site.register(Category, CategoryAdmin)
admin.site.register(HomepageBanner)
admin.site.register(HomesideBanner)
admin.site.register(ShoptopBanner)
admin.site.register(ShopbottomBanner)
admin.site.register(Reviews)
admin.site.register(Slider)
admin.site.register(Contact, ContactAdmin)
admin.site.register(Author)
admin.site.register(Wishlist)
admin.site.register(Newsletter)
admin.site.register(About)
admin.site.register(CustomUser)

admin.site.site_header = "St Royal's Stoi Admin"
admin.site.site_text = "St Royal's Admin Portal"
admin.site.site_title = "Welcome to St Royal Stoi Admin Portal"
