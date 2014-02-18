from django.conf.urls import *

urlpatterns = patterns('money.views',
    ('^regular_form/$', 'regular_form'),
    ('^regular_form/(?P<id>\d+)/$', 'regular_form_edit'),
    ('^model_form/$', 'model_form'),
    ('^model_form/(?P<id>\d+)/$', 'model_form_edit'),

)
