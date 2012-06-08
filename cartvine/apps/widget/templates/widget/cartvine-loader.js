//<!-- """ {"last_updated": "2012-06-02 17:30:00"} """ -->
//<!-- Check for http | https -- >
var cartvine_is_ready = true;
var App = void 0;
var url_scheme = window.parent.document.location.protocol + '//';
var shop_slug = window.Shopify.shop.replace('.myshopify.com','');
var shoppers_url = url_scheme + '{{ shoppers_app_domain }}/?shop=' + shop_slug;
// @NB - this url is tied to the widget:script named url; but must be maintained manually as it is a form of validation of the instantiating shopify cart
widget_list_object_url = url_scheme + '{{ shopify_app_domain}}/widget/script/'+ shop_slug +'/';

$.ajax({
    url: widget_list_object_url,
    dataType: 'script',
    cache: true,
    complete: function(xhr) { 
        if (xhr.status == 304) return;
    },
    error: function () {
    }
});
