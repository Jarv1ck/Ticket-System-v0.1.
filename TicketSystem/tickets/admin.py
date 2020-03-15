from django.contrib import admin

from .models import Product, Ticket, TicketComment, File


class InlineFileAdmin(admin.TabularInline):
    model = File


@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ('creator', 'product', 'subject',
                    'created', 'updated', 'status',
                    'responsible_user', )
    list_filter = ('product', 'status', 'created', 'responsible_user', )
    list_editable = ['status', 'responsible_user']
    search_fields = ['subject', 'product']

    inlines = [InlineFileAdmin]


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('title',)


@admin.register(TicketComment)
class TicketCommentAdmin(admin.ModelAdmin):
    list_display = ('creator', 'ticket', 'posted')
    list_filter = ('posted', )