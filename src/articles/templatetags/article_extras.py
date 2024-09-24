from django import template

register = template.Library()


@register.filter()
def get_value_bid(queryset):
    return queryset.get("bids")


@register.filter()
def get_value_user(queryset):
    return queryset.get("username")


@register.filter()
def get_value_article(queryset):
    return queryset.get("article")


@register.filter()
def get_image(queryset):
    queryset = str(queryset)
    return queryset[7:]


@register.filter()
def get_amount(queryset):
    queryset = str(queryset)
    return int(queryset[26:-3])


@register.filter()
def not_paid_article(queryset):
    return queryset["article"]


@register.filter()
def not_paid_bid(queryset):
    return queryset["bid"]
