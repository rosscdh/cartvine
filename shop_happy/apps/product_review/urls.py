from django.conf import settings
from django.conf.urls import patterns, include, url
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView


urlpatterns = patterns('',
    url(r'^shop/(?P<shop_slug>\w+)/(?P<product_slug>\w+)/$', TemplateView.as_view(template_name="product_review/default.html"), name='by_shop'),
    url(r'^create/(?P<product_slug>.*)/$', login_required(TemplateView.as_view(template_name="product_review/form.html"), settings.CUSTOMER_LOGIN_URL_NAME), name='create'),
    url(r'^reviewers/$', TemplateView.as_view(template_name="product_review/reviewers_list.html"), name='reviewers'),
    url(r'^$', TemplateView.as_view(template_name="product_review/productreview_list.html"), name='index'),
)
