//<!-- """ Javascript Widget for widget-auth-facebook.js """ -->

//<!-- Check for http | https -- >
var shop_slug = window.Shopify.shop.replace('.myshopify.com','');
var url_scheme = window.parent.document.location.protocol + '//';

// <!-- load required js files from shopify.app.cartvine.com/widgets/shop-url-extracted-from-shopify-store-page-object/: will return a json object of js files to load -- >
widget_list_object = url_scheme + '{{ request.get_host }}/widget/'+ shop_slug +'/'

$.getJSON(widget_list_object, function(data) {
    // Install Templates
    $.each(data.templates, function(index) {
        $(data.templates[index]).appendTo('head');
    });
    // Install Scripts
    $.each(data.widgets, function(index) {
        // $('<script/>', {
        //     id: 'cartvine-loader-js-' + index,
        //     src: data.widgets[index]
        // }).appendTo('body');
        $.getScript(data.widgets[index])
        .done(function(script, textStatus) {
            console.log( textStatus );
        })
        .fail(function(jqxhr, settings, exception) {
            alert('error')
        });  
    });
});
