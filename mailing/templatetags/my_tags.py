from django import template
from mailing.services import send_mailing

register = template.Library()


@register.filter()
def media_filter(path):
    if path:
        return f"/media/{path}"
    return "#"


@register.simple_tag
def send_mail(mailing_id):
    return send_mailing(mailing_id)
