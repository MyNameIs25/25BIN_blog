"""mySite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.conf.urls import url
from blog.feed import LatestEntriesFeed
from blog import views as blog_views
from django.contrib.sitemaps import GenericSitemap
from django.contrib.sitemaps.views import sitemap
from blog.models import Entry
import notifications.urls

info_dict = {
    'queryset': Entry.objects.all(),
    'date_field': 'modified_time',
}

urlpatterns = [
                  path('', blog_views.index),
                  path('admin/', admin.site.urls),
                  path('blog/', include('blog.urls')),
                  path('userprofile/', include('userprofile.urls', namespace='userprofile')),
                  path('comment/', include('comment.urls', namespace='comment')),
                  path('latest/feed/', LatestEntriesFeed()),
                  path('password-reset/', include('password_reset.urls')),
                  path('notice/', include('notice.urls', namespace='notice')),
                  path('inbox/notifications/', include(notifications.urls, namespace='notifications')),
                  path('sitemap.xml/', sitemap, {'sitemaps': {'blog': GenericSitemap(info_dict, priority=0.6)}}, name='django.contrib.sitemaps.views.sitemap'),
                  path('accounts/', include('allauth.urls')),
                  # path('comments/',include('django_comments.urls'))
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler403 = blog_views.permission_denied
handler404 = blog_views.page_not_found
handler500 = blog_views.page_error
