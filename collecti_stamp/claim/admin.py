from django.contrib import admin

from .models import Claim

# Register your models here.

def close_claim(modeladmin, request, queryset):
    queryset.update(closed=not queryset.first().closed)
    
close_claim.short_description = "Cambia estado de reclamación"
@admin.register(Claim)
class ClaimAdmin(admin.ModelAdmin):
    list_display = ('email', 'title', 'content','date', 'product', 'closed')
    list_editable =('closed',)
    search_fields = ('id',)
    readonly_fields = ('email', 'title', 'content','date', 'product',)
    actions=[close_claim]
    icon_name = 'comment'