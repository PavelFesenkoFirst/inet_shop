from django.contrib import admin

from apps.core.models import Category, Tag, Product, Contacts, ContactUs


class ProductInline(admin.TabularInline):
    model = Product
    # fields = ('title', 'price')
    extra = 0


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    inlines = [ProductInline]


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('title', 'price', 'category', 'in_stock')
    list_display_links = ('title', 'price', 'category')
    list_editable = ('in_stock',)


@admin.register(Contacts)
class ContactsAdmin(admin.ModelAdmin):
    pass


@admin.register(ContactUs)
class ContactUsAdmin(admin.ModelAdmin):
    pass


admin.site.register(Tag)
