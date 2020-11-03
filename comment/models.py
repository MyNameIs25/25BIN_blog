from django.db import models
from django.contrib.auth.models import User
from blog.models import Entry
from ckeditor.fields import RichTextField
from mptt.models import MPTTModel, TreeForeignKey


class Comment(MPTTModel):
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')
    reply_to = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE, related_name='replyers')
    article = models.ForeignKey(Entry, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    body = RichTextField()
    created_time = models.DateTimeField(auto_now_add=True)

    class MPTTMeta:
        order_insertion_by = ['created_time']

    def __str__(self):
        return self.body[:20]