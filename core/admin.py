from pyexpat import model
from django.contrib import admin
from django.utils.safestring import mark_safe
from .models import Category, Products, Order

admin.site.site_header = ("Мой склад")
# Register your models here.

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "url")
    list_display_links = ("name",)

@admin.register(Products)
class ProductsAdmin(admin.ModelAdmin):
    list_display = ("title", "category","draft")
    list_filter = ("category","kol")
    search_fields = ("title", "category__name")
    save_on_top = True
    save_as = True
    list_editable = ("draft",)
    actions = ["publish", "unpublish",]
    readonly_fields = ("get_image",)
    fieldsets = (
        (None, {
            "fields": (("title","category"),("image","price","kol"),)
        }),
        (None, {
            "fields": ("description", ("get_image"),)
        }),
        ("Options", {
            "fields": ("draft",)
        }),
    )

    def get_image(self, obj):
        return mark_safe(f'<img src={obj.poster.url} width="100" height="110"')

    def unpublish(self, request, queryset):
        row_update = queryset.update(draft=True)
        if row_update == 1:
            message_bit = "1 запись была обновлена"
        else:
            message_bit = f"{row_update} записей были обновлены"
        self.message_user(request, f"{message_bit}")

    def publish(self, request, queryset):
        row_update = queryset.update(draft=False)
        if row_update == 1:
            message_bit = "1 запись была обновлена"
        else:
            message_bit = f"{row_update} записей были обновлены"
        self.message_user(request, f"{message_bit}")

    publish.short_description = "Опубликовать"
    publish.allowed_permissions = ('change', )

    unpublish.short_description = "Снять с публикации"
    unpublish.allowed_permissions = ('change',)

    get_image.short_description = "Постер"



admin.site.register(Order)