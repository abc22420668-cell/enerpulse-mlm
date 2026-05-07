from django.db import models
from django.utils.translation import gettext_lazy as _


class Category(models.Model):
    """Product category."""
    name = models.CharField(max_length=200, verbose_name=_('Name'))
    name_en = models.CharField(max_length=200, blank=True, verbose_name=_('Name (EN)'))
    name_zh_hant = models.CharField(max_length=200, blank=True, verbose_name=_('Name (ZH-Hant)'))
    name_zh_hans = models.CharField(max_length=200, blank=True, verbose_name=_('Name (ZH-Hans)'))
    slug = models.SlugField(max_length=200, unique=True)
    description = models.TextField(blank=True, verbose_name=_('Description'))
    image = models.ImageField(upload_to='categories/', null=True, blank=True)
    sort_order = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = _('Category')
        verbose_name_plural = _('Categories')
        ordering = ['sort_order', 'name']
    
    def __str__(self):
        return self.name


class Product(models.Model):
    """Product model with MLM PV tracking."""
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True, blank=True,
        related_name='products', verbose_name=_('Category'),
    )
    
    # Multi-language fields
    name = models.CharField(max_length=300, verbose_name=_('Name'))
    name_en = models.CharField(max_length=300, blank=True, verbose_name=_('Name (EN)'))
    name_zh_hant = models.CharField(max_length=300, blank=True, verbose_name=_('Name (ZH-Hant)'))
    name_zh_hans = models.CharField(max_length=300, blank=True, verbose_name=_('Name (ZH-Hans)'))
    description = models.TextField(blank=True, verbose_name=_('Description'))
    description_en = models.TextField(blank=True, verbose_name=_('Description (EN)'))
    description_zh_hant = models.TextField(blank=True, verbose_name=_('Description (ZH-Hant)'))
    description_zh_hans = models.TextField(blank=True, verbose_name=_('Description (ZH-Hans)'))
    
    slug = models.SlugField(max_length=200, unique=True)
    sku = models.CharField(max_length=100, unique=True, verbose_name='SKU')
    
    # Pricing
    price_usd = models.DecimalField(
        max_digits=12, decimal_places=2,
        verbose_name=_('Price (USD)'),
    )
    pv = models.IntegerField(
        default=0,
        verbose_name=_('PV'),
        help_text=_('Product Value points for MLM calculations'),
    )
    
    # Inventory
    stock = models.IntegerField(default=0, verbose_name=_('Stock'))
    is_active = models.BooleanField(default=True, verbose_name=_('Active'))
    is_featured = models.BooleanField(default=False, verbose_name=_('Featured'))
    
    # Images
    image = models.ImageField(upload_to='products/', null=True, blank=True)
    image_2 = models.ImageField(upload_to='products/', null=True, blank=True)
    image_3 = models.ImageField(upload_to='products/', null=True, blank=True)
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = _('Product')
        verbose_name_plural = _('Products')
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.name} (${self.price_usd})"
    
    def get_name(self, lang_code=None):
        """Get product name in the specified language."""
        if not lang_code:
            from django.utils.translation import get_language
            lang_code = get_language()
        
        mapping = {
            'en': self.name_en,
            'zh-Hant': self.name_zh_hant,
            'zh-Hans': self.name_zh_hans,
        }
        return mapping.get(lang_code) or self.name
    
    def get_description(self, lang_code=None):
        """Get product description in the specified language."""
        if not lang_code:
            from django.utils.translation import get_language
            lang_code = get_language()
        
        mapping = {
            'en': self.description_en,
            'zh-Hant': self.description_zh_hant,
            'zh-Hans': self.description_zh_hans,
        }
        return mapping.get(lang_code) or self.description
