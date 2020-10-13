from django.contrib import admin

# Register your models here.
from .models import Invoice


class InvoicesAdmin(admin.ModelAdmin):
    
    list_select_related = True
    list_display=['character','invoice_ref', 'amount']
    search_fields = ('character', 'invoice_ref')
    raw_id_fields = ('character', 'payment')
    
admin.site.register(Invoice, InvoicesAdmin)