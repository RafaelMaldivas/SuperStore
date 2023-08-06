from django.contrib import admin
from .models import Account
from django.contrib.auth.admin import UserAdmin

# Register your models here.
class AccountAdmin(UserAdmin):
    list_display = ('email', 'primeiro_nome', 'ultimo_nome', 'username', 'ultimo_login', 'data_de_entrada', 'is_active' )
    list_display_links = ('email', 'primeiro_nome', 'username')
    readonly_fields = ('ultimo_login', 'data_de_entrada')
    ordering = ('-data_de_entrada',)

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()

admin.site.register(Account, AccountAdmin)