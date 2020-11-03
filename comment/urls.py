from django.urls import path
from . import views

app_name = 'comment'

urlpatterns = [
    path('post-comment/<int:article_id>/', views.post_comment, name='post_comment'),# 发表评论
    path('post-comment/<int:article_id>/<int:parent_comment_id>', views.post_comment, name='comment_reply') #二级评论
]

