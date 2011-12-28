
from django.conf.urls.defaults import patterns, url, include
from conf_center.views import ObjectStoreRoot, StoredObject, simplequeue, simplequeueroot, RestRoot
from django.contrib import admin
admin.autodiscover()
 
urlpatterns = patterns('conf_center.views',
     (r'^admin/', include(admin.site.urls)),
    url(r'^$', RestRoot.as_view(), name='object-store-root'),             
    url(r'^config$', ObjectStoreRoot.as_view(), name='object-store-root'), 
    url(r'^config/(?P<key>[A-Za-z0-9_-]{1,64})/$', StoredObject.as_view(), name='stored-object'),
    url(r'^queue/$', simplequeueroot.as_view(), name='rqueue-root'), 
    url(r'^queue/(?P<qname>[A-Za-z0-9_-]*)/$', simplequeue.as_view(), name="rqueue")
)
