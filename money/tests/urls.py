from django.conf.urls import *

from money.tests.views import *

urlpatterns = patterns(
    '',
    ('^instance-view/$', instance_view),
    ('^model-view/$', model_view),
    ('^model-save-view/$', model_from_db_view),
    ('^model-form-view/$', model_form_view),

    ('^regular_form/$', regular_form),
    ('^regular_form/(?P<id>\d+)/$', regular_form_edit),
    ('^model_form/(?P<id>\d+)/$', model_form_edit),
)
