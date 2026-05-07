from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from .models import Category, Product


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'sort_order', 'is_active', 'created_at')
    list_filter = ('is_active',)
    search_fields = ('name', 'name_en', 'name_zh_hant', 'name_zh_hans')
    prepopulated_fields = {'slug': ('name',)}
    list_editable = ('sort_order', 'is_active')
    
    fieldsets = (
        (None, {
            'fields': ('name', 'slug', 'description', 'image')
        }),
        (_('Multi-language Names'), {
            'fields': ('name_en', 'name_zh_hant', 'name_zh_hans'),
            'classes': ('collapse',),
        }),
        (_('Settings'), {
            'fields': ('sort_order', 'is_active'),
        }),
    )


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        'name', 'sku', 'category', 'price_usd', 'pv',
        'stock', 'is_active', 'is_featured', 'created_at'
    )
    list_filter = ('is_active', 'is_featured', 'category')
    search_fields = ('name', 'name_en', 'name_zh_hant', 'name_zh_hans', 'sku')
    prepopulated_fields = {'slug': ('name',)}
    list_editable = ('price_usd', 'pv', 'stock', 'is_active', 'is_featured')
    
    fieldsets = (
        (None, {
            'fields': (
                'category', 'name', 'slug', 'sku',
                'description', 'image',
            )
        }),
        (_('Multi-language Names'), {
            'fields': (
                'name_en', 'name_zh_hant', 'name_zh_hans',
                'description_en', 'description_zh_hant', 'description_zh_hans',
            ),
            'classes': ('collapse',),
        }),
        (_('Pricing & MLM'), {
            'fields': ('price_usd', 'pv'),
        }),
        (_('Inventory'), {
            'fields': ('stock', 'is_active', 'is_featured'),
        }),
        (_('Additional Images'), {
            'fields': ('image_2', 'image_3'),
            'classes': ('collapse',),
        }),
    )
    
    actions = ['activate_products', 'deactivate_products']
    
    def activate_products(self, request, queryset):
        queryset.update(is_active=True)
    activate_products.short_description = _('Activate selected products')
    
    def deactivate_products(self, request, queryset):
        queryset.update(is_active=False)
    deactivate_products.short_description = _('Deactivate selected products')
