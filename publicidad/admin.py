from django.contrib import admin
from .models import Suscription, Negocio, Promotion, Category


class NegocioAdmin(admin.ModelAdmin):
    """docstring for NegocioAdmin"""
    exclude = ('owner', 'suscription', )

    def get_queryset(self, request):
        query = super(NegocioAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return query
        return query.filter(owner=request.user)

admin.site.register(Negocio, NegocioAdmin)


class PromoAdmin(admin.ModelAdmin):
    '''
        Admin View for Promotion Model
    '''
    exclude = ('negocio',)

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

admin.site.register(Promotion, PromoAdmin)


class CategoriesAdmin(admin.ModelAdmin):
    '''
        Admin View for Categories
    '''
    exclude = ('negocio',)

    def get_queryset(self, request, queryset):
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

admin.site.register(Category, CategoriesAdmin)

# Register your models here.
# superuser can add/edit/delete suscription type items
admin.site.register(Suscription)
