//<!-- """ Javascript Widget for widget-auth-facebook.js """ -->

//<!-- Check for http | https -- >
var cartvine_is_ready = true;
var App = void 0;
var url_scheme = window.parent.document.location.protocol + '//';
var shop_slug = window.Shopify.shop.replace('.myshopify.com','');
var shoppers_url = url_scheme + '{{ shoppers_app_domain }}/?shop=' + shop_slug;
// @NB - this url is tied to the widget:script named url; but must be maintained manually as it is a form of validation of the instantiating shopify cart
widget_list_object = url_scheme + '{{ shopify_app_domain}}/widget/script/'+ shop_slug +'/';

$.getJSON(widget_list_object, function(data) {
    // Install Templates
    $.each(data.templates, function(index) {
        $(data.templates[index]).appendTo('head');
    });

    // Install Scripts
    $.ajaxSetup({ cache: true });

    $.each(data.widgets, function(index) {
        url = data.widgets[index];
        $.ajax({
            url: url,
            dataType: 'script',
            cache: true,
            complete: function(xhr) { 
                if (typeof Em != 'undefined') {
                    // Create the EmberJs Application which is shared between widgets
                    // @TODO create object with event handlers to initialize CartVine objects
                    App = Em.Application.create();
                };
                if (typeof App != 'undefined' && typeof DS != 'undefined' && typeof DS.DjangoTastypieAdapter != 'undefined') {
                    App.store = DS.Store.create({
                      revision: 4,
                      adapter: DS.DjangoTastypieAdapter.create({
                        serverDomain: url_scheme + "{{ request.get_host }}/",
                        tastypieApiUrl: "api/v1/"
                      })
                    });
                };
                if (xhr.status == 304) return;
            },
            error: function () {
                cartvine_is_ready = false;
            }
        });
    });
});
