from django.contrib import admin
from django.utils.translation import ugettext as _
# from django.views.decorators.cache import never_cache
from .models import Suscription, Negocio, Promotion, Category, Product


class SiteManager(admin.AdminSite):
    """My custom admin site for Administrator"""
    site_header = _('GastroNica, Manage your stuffs')
    site_title = _('Gastronica Management')
    index_title = _('Gastronica')
    login_template = 'auth/login.html'

mi_contenido = SiteManager('Administrator Site')


class NegocioAdmin(admin.ModelAdmin):
    """docstring for NegocioAdmin"""
    exclude = ('owner', 'suscription', )

    def get_queryset(self, request):
        query = super(NegocioAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return query
        return query.filter(owner=request.user)

# admin.site.register(Negocio, NegocioAdmin)
mi_contenido.register(Negocio, NegocioAdmin)


class PromoAdmin(admin.ModelAdmin):
    '''
        Admin View for Promotion Model
    '''
    exclude = ('negocio',)
    list_filter = ('is_active',)

    def get_queryset(self, request):
        query = super(PromoAdmin, self).get_queryset(request)

        if request.user.is_superuser:
            return query

        return query.filter(negocio__owner=request.user)

    def save_model(self, request, obj, form, change):
        ''' just assign the negocio owned by its admin'''
        if getattr(self, 'negocio', None) is None:
            negocio = Negocio.objects.get(owner=request.user)
            obj.negocio = negocio
        obj.save()

# admin.site.register(Promotion, PromoAdmin)
mi_contenido.register(Promotion, PromoAdmin)


class CategoriesAdmin(admin.ModelAdmin):
    '''
        Admin View for Categories
    '''
    exclude = ('negocio',)

    def get_queryset(self, request):
        query = super(CategoriesAdmin, self).get_queryset(request)

        if request.user.is_superuser:
            return query

        return query.filter(negocio__owner=request.user)

    def save_model(self, request, obj, form, change):
        ''' just assign the negocio owned by its admin'''
        if getattr(self, 'negocio', None) is None:
            negocio = Negocio.objects.get(owner=request.user)
            obj.negocio = negocio
        obj.save()

# admin.site.register(Category, CategoriesAdmin)
mi_contenido.register(Category, CategoriesAdmin)


class category_filter(admin.SimpleListFilter):
    """shows the negocio's categories on product filters"""

    title = _('Categories')
    parameter_name = 'category'

    def lookups(self, request, model_admin):
        category_list = []
        queryset = Category.objects.filter(negocio__owner=request.user)
        for category in queryset:
            category_list.append(
                (str(category.id), category.name)
            )

        return sorted(category_list, key=lambda tp: tp[1])

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(category_id=self.value())
        return queryset


class ProductsAdmin(admin.ModelAdmin):
    '''
        Admin View for Products
    '''
    list_display = ('name', 'price', 'category')
    list_filter = (category_filter,)
    # raw_id_fields = ('',)
    # readonly_fields = ('',)
    # search_fields = ('',)

    def get_queryset(self, request):
        query = super(ProductsAdmin, self).get_queryset(request)

        if request.user.is_superuser:
            return query

        return query.filter(category__negocio__owner=request.user)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        """this filter the categories availables on product edits or create"""
        if db_field.name == "category":
            kwargs["queryset"] = Category.objects.filter(
                negocio__owner=request.user
            )
            return super(ProductsAdmin, self).formfield_for_foreignkey(
                db_field, request, **kwargs
            )

# admin.site.register(Product, ProductsAdmin)
mi_contenido.register(Product, ProductsAdmin)

# Register your models here.
# superuser can add/edit/delete suscription type items
mi_contenido.register(Suscription)
