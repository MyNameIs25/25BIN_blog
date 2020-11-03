from django.contrib.syndication.views import Feed
# from django.urls import reverse
from .models import Entry


class LatestEntriesFeed(Feed):
    title = "25BIN"
    link = '/siteblogs/'
    description = "最新的文章！"

    def items(self):
        return Entry.objects.order_by('-created_time')[:5]

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return item.abstract

    # def item_link(self, item):
    #     return reverse('blog:blog_detail', kwargs={'blog_id':item.id})
