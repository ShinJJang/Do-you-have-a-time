from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'webapp.views.home', name='home'),
    url(r'^make/', 'webapp.views.make', name='make'),
    url(r'^edit/(?P<planid>\w{0,50})/$', 'webapp.views.edit', name='edit'),
    url(r'^done/', 'webapp.views.done', name='done'),
    url(r'^result/(?P<planid>\w{0,50})/$', 'webapp.views.result', name='result'),
    url(r'^login/', 'webapp.views.login', name='login'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
)
