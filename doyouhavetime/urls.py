from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'webapp.views.home', name='home'),
    url(r'^done/', 'webapp.views.done', name='done'),
    url(r'^result/', 'webapp.views.result', name='result'),
    url(r'^login/', 'webapp.views.login', name='login'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
)
