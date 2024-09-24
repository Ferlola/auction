from django import template

register = template.Library()


@register.filter()
def get_value_user(queryset):
    return queryset.get("username")


@register.filter()
def get_bid(value):
    value = str(value)
    return value[20:-4]


@register.filter()
def get_fee(value1, value2):
    value1 = float(value1) / 100
    value2 = float(value2)
    return (value1 * value2) + value2


@register.filter()
def get_decimal(value):
    value = str(value)
    return value[0:-3]
