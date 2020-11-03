from django import template
from ..models import Entry, ArticleColumn
from django.utils import timezone
import math

register = template.Library()


@register.simple_tag
def get_recent_entries(num=5):
    return Entry.objects.all().order_by('-created_time')[:num]


@register.simple_tag
def get_popular_entries(num=5):
    return Entry.objects.all().order_by('-visited')[:num]


@register.simple_tag
def archives():
    return Entry.objects.dates('created_time', 'month', order='DESC')


@register.simple_tag
def get_entry_count_of_date(year, month):
    return Entry.objects.filter(created_time__year=year, created_time__month=month).count()


@register.simple_tag
def get_tags():
    return Entry.tags


@register.simple_tag
def get_columns():
    return ArticleColumn.objects.all()


@register.filter(name='timesince_zh')
def time_since_zh(value):
    now = timezone.now()
    diff = now - value

    if diff.days == 0 and 0 <= diff.seconds < 60:
        return '刚刚'

    if diff.days == 0 and 60 <= diff.seconds < 3600:
        return str(math.floor(diff.seconds / 60)) + "分钟前"

    if diff.days == 0 and 3600 <= diff.seconds < 86400:
        return str(math.floor(diff.seconds / 3600)) + "小时前"

    if 1 <= diff.days < 30:
        return str(diff.days) + "天前"

    if 30 <= diff.days < 365:
        return str(math.floor(diff.days / 30)) + "个月前"

    if diff.days >= 365:
        return str(math.floor(diff.days / 365)) + "年前"

