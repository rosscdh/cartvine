//<!-- """ Javascript Widget for widget-auth-facebook.js """ -->

//<!-- Check for http | https -- >
var cartvine_is_ready = true;

var url_scheme = window.parent.document.location.protocol + '//';
var shop_slug = window.Shopify.shop.replace('.myshopify.com','');
var shoppers_url = url_scheme + '{{ shoppers_app_domain }}/?shop=' + shop_slug;

widget_list_object = url_scheme + '{{ shopify_app_domain}}/widget/'+ shop_slug +'/';

$.getJSON(widget_list_object, function(data) {
    // Install Templates
    $.each(data.templates, function(index) {
        $(data.templates[index]).appendTo('head');
    });

    // Install Scripts
    $.ajaxSetup({ cache: true });

    $.each(data.widgets, function(index) {
        $.ajax({
            url: data.widgets[index],
            dataType: 'script',
            cache: true,
            complete: function(xhr) { 
                if (xhr.status == 304) return;
            },
            error: function () {
                cartvine_is_ready = false;
            }
        });
    });
});
