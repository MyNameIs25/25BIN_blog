from django.shortcuts import render, get_object_or_404, render_to_response, redirect
from django.views import View
from comment.forms import CommentForm
from comment.models import Comment
from . import models
import markdown
from django.http import HttpResponse
from .forms import ArticlePostForm
from django.contrib.auth.models import User
import pygments
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Q
# from django_comments.models import Comment
from .models import Entry, ArticleColumn


def make_paginator(objects, page, num=5):
    paginator = Paginator(objects, num)
    try:
        object_list = paginator.page(page)
    except PageNotAnInteger:
        object_list = paginator.page(1)
    except EmptyPage:
        object_list = paginator.page(paginator.num_pages)
    return object_list, paginator


def pagination_data(paginator, page):
    """
    用于自定义展示分页页码的方法
    :param paginator: Paginator类的对象
    :param page: 当前请求的页码
    :return: 一个包含所有页码和符号的字典
    """
    # 如果无法分页，也就是只有一页，则无需显示分页导航条，不需要任何分页导航条的数据，返回空字典。
    if paginator.num_pages == 1:
        return {}
    # 当前页左边连续的页码号，初始值为空。
    left = []
    # 当前页右边连续的页号号，初始值为空。
    right = []
    # 标示第一页页码后是否需要显示省略号
    left_has_more = False
    # 标示第一页页码前是否需要显示省略号
    right_has_more = False

    # 标示是否需要显示第1页的页码号
    first = False
    # 标示是否需要显示最后一页的页码号
    last = False

    try:
        page_number = int(page)
    except ValueError:
        page_number = 1
    except:
        page_number = 1

    # 获取分页后的总页数
    total_pages = paginator.num_pages

    # 获取整个分页页码列表，比如分了4页，则为[1, 2, 3, 4]
    page_range = paginator.page_range

    if page_number == 1:
        # 如果请求的是第一页的数据，这当前页左边不需要数据，因此left=[]。
        # 此时只要获取当前页右边的页码
        # 比如分页页码列表是[1, 2, 3, 4]，那么获取的就是right = [2, 3]。
        # 注意这里只获取了当前页码后连续两个页码
        right = page_range[page_number:page_number + 4]

        if right[-1] < total_pages - 1:
            right_has_more = True
        if right[-1] < total_pages:
            last = True
    elif page_number == total_pages:
        # 如果请求的是最后一页，则right = []。
        left = page_range[(page_number - 3) if (page_number - 3) > 0 else 0:page_number - 1]
        if left[0] > 2:
            left_has_more = True
        if left[0] > 1:
            first = True
    else:
        left = page_range[(page_number - 3) if (page_number - 3) > 0 else 0:page_number - 1]
        right = page_range[page_number:page_number + 2]
        if right[-1] < total_pages - 1:
            right_has_more = True
        if right[-1] < total_pages:
            last = True
        if left[0] > 2:
            left_has_more = True
        if left[0] > 1:
            first = True

    data = {
        'left': left,
        'right': right,
        'left_has_more': left_has_more,
        'right_has_more': right_has_more,
        'first': first,
        'right': right,
    }

    return data


# Create your views here.
def index(request):
    entries = models.Entry.objects.all()
    page = request.GET.get('page', 1)
    entry_list, paginator = make_paginator(entries, page)
    page_data = pagination_data(paginator, page)

    return render(request, 'blog/index.html', locals())


def detail(request, blog_id):
    # entry = models.Entry.objects.get(id=blog_id)
    entry = get_object_or_404(models.Entry, id=blog_id)
    entry.increase_visited()
    md = markdown.Markdown(extensions=[
        'markdown.extensions.extra',
        'markdown.extensions.codehilite',
        'markdown.extensions.toc',
    ])
    entry.body = md.convert(entry.body)
    entry.toc = md.toc
    comment_form = CommentForm()
    comments = Comment.objects.filter(article=blog_id)

    return render(request, 'blog/detail.html', locals())


def column(request, column_id):
    # c = models.Category.objects.get(id=category_id)
    c = get_object_or_404(models.ArticleColumn, id=column_id)
    entries = models.Entry.objects.filter(column=c)
    page = request.GET.get('page', 1)
    entry_list, paginator = make_paginator(entries, page)
    page_data = pagination_data(paginator, page)

    return render(request, 'blog/index.html', locals())


def tag(request):
    t = request.GET.get('tag')
    entries = Entry.objects.all()
    if t and t != 'None':
        entries = entries.filter(tags__name__in=[t])
    page = request.GET.get('page', 1)
    entry_list, paginator = make_paginator(entries, page)
    page_data = pagination_data(paginator, page)
    return render(request, 'blog/index.html', locals())


def search(request):
    keyword = request.GET.get('keyword', None)
    if not keyword:
        error_msg = "请输入关键字"
        return render(request, 'blog/index.html', locals())

    entries = models.Entry.objects.filter(
        Q(title__icontains=keyword) | Q(body__icontains=keyword) | Q(abstract__icontains=keyword))
    page = request.GET.get('page', 1)
    entry_list, paginator = make_paginator(entries, page)
    page_data = pagination_data(paginator, page)
    return render(request, 'blog/index.html', locals())


def archives(request, year, month):
    entries = models.Entry.objects.filter(created_time__year=year, created_time__month=month)
    page = request.GET.get('page', 1)
    entry_list, paginator = make_paginator(entries, page)
    page_data = pagination_data(paginator, page)
    return render(request, 'blog/index.html', locals())


def article_create(request):
    # 判断用户是否提交数据
    if request.method == "POST":
        # 将提交的数据赋值到表单实例中
        article_post_form = ArticlePostForm(data=request.POST)
        # 判断提交的数据是否满足模型的要求
        if article_post_form.is_valid():
            # 保存数据，但暂时不提交到数据库中
            new_article = article_post_form.save(commit=False)
            # 指定数据库中 id=1 的用户为作者
            # 如果你进行过删除数据表的操作，可能会找不到id=1的用户
            # 此时请重新创建用户，并传入此用户的id
            new_article.author = User.objects.get(id=request.user.id)
            if request.POST['column'] != 'none':
                new_article.column = ArticleColumn.objects.get(id=request.POST['column'])
            # 将新文章保存到数据库中
            new_article.save()
            article_post_form.save_m2m()
            # 完成后返回到文章列表
            return redirect("blog:blog_index")
        # 如果数据不合法，返回错误信息
        else:
            return HttpResponse("表单内容有误，请重新填写。")
    # 如果用户请求获取数据
    else:
        # 创建表单类实例
        article_post_form = ArticlePostForm()
        columns = ArticleColumn.objects.all()
        # 赋值上下文
        context = {'article_post_form': article_post_form, 'columns': columns}
        # 返回模板
        return render(request, 'blog/create.html', context)


def article_safe_delete(request, id):
    if request.method == 'POST':
        article = Entry.objects.get(id=id)
        article.delete()
        return redirect("blog:blog_index")
    else:
        return HttpResponse("仅允许post请求")


# 更新文章
def article_update(request, id):
    """
    更新文章的视图函数
    通过POST方法提交表单，更新titile、body字段
    GET方法进入初始表单页面
    id： 文章的 id
    """

    # 获取需要修改的具体文章对象
    article = Entry.objects.get(id=id)
    # 判断用户是否为 POST 提交表单数据
    if request.method == "POST":
        # 将提交的数据赋值到表单实例中
        article_post_form = ArticlePostForm(request.POST, request.FILES)
        # 判断提交的数据是否满足模型的要求
        if article_post_form.is_valid():
            # 保存新写入的 title、body 数据并保存
            article.cd = article_post_form.cleaned_data
            article.title = article.cd['title']
            article.body = article.cd['body']
            article.abstract = article.cd['abstract']
            if 'img' in request.FILES:
                article.img = article.cd["img"]
            if request.POST['column'] != 'none':
                article.column = ArticleColumn.objects.get(id=request.POST['column'])
            else:
                article.column = None
            article.save()
            # 完成后返回到修改后的文章中。需传入文章的 id 值
            return redirect("blog:blog_detail", blog_id=id)
        # 如果数据不合法，返回错误信息
        else:
            return HttpResponse("表单内容有误，请重新填写。")

    # 如果用户 GET 请求获取数据
    else:
        # 创建表单类实例
        article_post_form = ArticlePostForm()
        columns = ArticleColumn.objects.all()
        # 赋值上下文，将 article 文章对象也传递进去，以便提取旧的内容
        context = {'article': article, 'article_post_form': article_post_form, 'columns': columns}
        # 将响应返回到模板中
        return render(request, 'blog/update.html', context)


def permission_denied(request, exception, template_name="403.html"):
    response = render(request, 'blog/403.html', locals())
    response.status_code = 403
    return response


def page_not_found(request, exception, template_name="404.html"):
    response = render(request, 'blog/404.html', locals())
    response.status_code = 404
    return response


def page_error(request, template_name="500.html"):
    response = render(request, 'blog/500.html', locals())
    response.status_code = 500
    return response


class IncreaseLikesView(View):
    def post(self, request, *args, **kwargs):
        article = Entry.objects.get(id=kwargs.get('id'))
        article.likes += 1
        article.save()
        return HttpResponse('success')