from django.conf import settings
from django.conf.urls import patterns, include, url
from cartvine.utils import login_required
from django.views.generic import ListView, TemplateView, DetailView

from models import CartvineEmail

urlpatterns = patterns('',
    url(r'^(?P<pk>\d+)/$', login_required(DetailView.as_view(queryset=CartvineEmail.objects.all())), name='info'),
    url(r'^$', ListView.as_view(queryset=CartvineEmail.objects.all(), template_name="mail/mail_list.html"), name='index'),
)
