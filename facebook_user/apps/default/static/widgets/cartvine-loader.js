//<!-- """ Javascript Widget for widget-auth-facebook.js """ -->

//<!-- Check for http | https -- >
var shop_slug = window.Shopify.shop.replace('.myshopify.com','');
var url_scheme = window.parent.document.location.protocol + '//';
url_scheme = '//';
// <!-- load required js files from shopify.app.cartvine.com/widgets/shop-url-extracted-from-shopify-store-page-object/: will return a json object of js files to load -- >
widget_list_object = url_scheme + 'localhost:8000/widgets/'+ shop_slug +'/'

$.getJSON(widget_list_object, function(data) {
    var items = []
  $.each(data, function(key, val) {
    console.log(key)
    items.push('<li id="' + key + '">' + val + '</li>');
  });

  $('<ul/>', {
    'class': 'my-new-list',
    html: items.join('')
  }).appendTo('body');
});

var oHead = document.getElementsByTagName('BODY').item(0);
var oScript = '';

// oScript = document.createElement("script");
// oScript.id = "cartvine-loader";
// oScript.type = "text/javascript";
// oScript.src = widget_list_object;
// oHead.appendChild(oScript);

// oScript = '';


scripts = {
    'widgets': ['http://localhost:8001/static/widgets/widget-auth-facebook.js']
};
// <!-- setup local js object to load the provided remote scripts --> 


// loop over provided script urls and install them locally
if (scripts['widgets'].length > 0) {
    for (index in scripts['widgets']) {
        remote_script = scripts['widgets'][index];

        oScript = document.createElement("script");
        oScript.type = "text/javascript";
        oScript.src = remote_script;

        oHead.appendChild(oScript);
    };
}
