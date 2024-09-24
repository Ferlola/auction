from django import template

register = template.Library()


@register.filter()
def get_value_user(queryset):
    return queryset.get()


@register.filter()
def get_value_paid(queryset):
    return queryset.get()
