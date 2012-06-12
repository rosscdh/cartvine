from django.conf.urls import patterns, include, url
from cartvine.utils import login_required
from django.views.generic import TemplateView

from views import CustomerListView, CustomerDetailView

LoginView = TemplateView.as_view(template_name="customer/default.html")


urlpatterns = patterns('',
    url(r'^login/$', LoginView, name='login'),
    url(r'^(?P<pk>\d+)/$', login_required(CustomerDetailView.as_view()), name='info'),
    url(r'^$', login_required(CustomerListView.as_view()), name='index'),
)
