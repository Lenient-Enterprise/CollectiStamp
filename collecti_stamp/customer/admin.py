from django.contrib import admin

from .models import User


# Register your models here.
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'email_verified', 'address', 'delivery_method', 'payment_method')
    list_filter = ['email_verified']
    search_fields = ('username', 'email')
    ordering = ('username',)
    fieldsets = (
        (None, {'fields': ('username', 'email',)}),
        ('Permissions', {'fields': ['email_verified']}),
    )
    icon_name = 'person'