from django.contrib import admin

from .models import Claim

# Register your models here.
@admin.register(Claim)
class ClaimAdmin(admin.ModelAdmin):
    list_display = ('username', 'title', 'content','date', 'product')
    search_fields = ('id',)
    icon_name = 'comment'