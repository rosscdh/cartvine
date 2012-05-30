//<!-- """ Javascript Widget for widget-auth-facebook.js """ -->

//<!-- Check for http | https -- >
var shop_slug = window.Shopify.shop.replace('.myshopify.com','');
var url_scheme = window.parent.document.location.protocol + '//';
url_scheme = '//';

// <!-- load required js files from shopify.app.cartvine.com/widgets/shop-url-extracted-from-shopify-store-page-object/: will return a json object of js files to load -- >
widget_list_object = url_scheme + 'localhost:8000/widget/'+ shop_slug +'/'

$.getJSON(widget_list_object, function(data) {
    $.each(data.templates, function(index) {
        data.templates[index].appendTo('head');
        //console.log(data.templates[index])
    });
    $.each(data.widgets, function(index) {
        $('<script/>', {
            src: data.widgets[index]
        }).appendTo('body');
    });
});

var oHead = document.getElementsByTagName('BODY').item(0);
var oScript = '';
