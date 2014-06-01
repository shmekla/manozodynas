from django.conf.urls import patterns, url
from django.conf import settings

from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from .views import index_view, login_view, WordAdd, WordList, TranslationAdd

urlpatterns = patterns('',
    url(r'^$', index_view, name='index'),
    url(r'^login$', login_view, name='login'),
    url(r'^add$', WordAdd.as_view(), name='add'),
    url(r'^list$', WordList.as_view(), name='list'),
    url(r'^(?P<id>\d+)/translation$', TranslationAdd.as_view(), name='add-tra'),
)

urlpatterns += staticfiles_urlpatterns()
urlpatterns += patterns('',
    (r'^media/(?P<path>.*)$', 'django.views.static.serve',
     {'document_root': settings.MEDIA_ROOT}),
)
