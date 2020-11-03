
from django.db import models
from django.contrib.auth.models import User
from taggit.managers import TaggableManager
# Create your models here.
from django.urls import reverse
from django.utils import timezone


# class Category(models.Model):
#     name = models.CharField(max_length=128, verbose_name="博客分类")
#
#     def __str__(self):
#         return self.name
#
#     class Meta:
#         verbose_name = "博客分类"
#         verbose_name_plural = "博客分类"
#
#
# class Tag(models.Model):
#     name = models.CharField(max_length=128, verbose_name="博客标签")
#
#     def __str__(self):
#         return self.name
#
#     class Meta:
#         verbose_name = "博客标签"
#         verbose_name_plural = "博客标签"


class ArticleColumn(models.Model):
    """
    栏目的 Model
    """
    # 栏目标题
    title = models.CharField(max_length=100, blank=True)
    # 创建时间
    created = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title


class Entry(models.Model):
    title = models.CharField(max_length=128, verbose_name="文章标题")
    author = models.ForeignKey(User, on_delete=True, verbose_name="博客作者")
    img = models.ImageField(upload_to='blog_images/%Y%m%d/', null=True, blank=True, verbose_name="博客配图")
    body = models.TextField(verbose_name="博客正文")
    abstract = models.TextField(max_length=256, blank=True, null=True, verbose_name="博客摘要")
    visited = models.PositiveIntegerField(default=0, verbose_name="博客访问量")
    likes = models.PositiveIntegerField(default=0)
    tags = TaggableManager(blank=True)
    column = models.ForeignKey(ArticleColumn, null=True, blank=True, on_delete=models.CASCADE, related_name='article')
    created_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    modified_time = models.DateTimeField(auto_now=True, verbose_name="修改时间")

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('blog:blog_detail', kwargs={'blog_id': self.id})  # http://127.0.0.1/blog/blog_id

    def increase_visited(self):
        self.visited += 1
        self.save(update_fields=['visited'])

    def was_created_recently(self):
        # 若文章是"最近"发表的，则返回 True
        diff = timezone.now() - self.created
        # if diff.days <= 0 and diff.seconds < 60:
        if diff.days == 0 and 0 <= diff.seconds < 60:
            return True
        else:
            return False

    class Meta:
        ordering = ['-created_time']
        verbose_name = "博客"
        verbose_name_plural = "博客"




