from django.conf.urls import patterns, include, url
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView

LoginView = TemplateView.as_view(template_name="customer/default.html")

urlpatterns = patterns('',
    url(r'^login/$', LoginView, name='login'),
    url(r'^$', LoginView, name='index'),
)
