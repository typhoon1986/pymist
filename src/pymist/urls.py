
from django.conf.urls.defaults import patterns, url
from bot.views import do
 
urlpatterns = patterns('conf_center.views',
    ('[A-Za-z]*\.do$', do),
)
