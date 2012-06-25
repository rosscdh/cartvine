{% load url from future %}
self.App.get('/products/:slug.html', function (req) {

    var slug = req.params['slug'].replace('.html', '');
    var url = self.buildUrl('/api/v1/product/?slug=' + slug);

    $.getJSON(url, function(data) {
        product = data.objects[0];

        var variationControlsView = function() {
            var source   = $("script#variation-controls").html();
            var context = {
                'product': product,
            };
            var template = Handlebars.compile(source);
            return template(context);
        };

        self.injectView(variationControlsView(), '{{ widget.widget_js_name }}', '{{ config.variations.target_id }}');

        // list of properties
        var url = self.buildUrl('/api/v1/variant/?product=' + product.id);
        $.getJSON(url, function(data) {
            variant_list = data.objects;
            var productPropertiesView = function(sam) {
                var source   = $("script#product-properties").html();
                var context = {
                    'product': product,
                    'variant_list': variant_list,
                };
                var template = Handlebars.compile(source);
                return template(context);
            };
            self.injectView(productPropertiesView(), '{{ widget.widget_js_name }}', '{{ config.products.target_id }}');
        })
    })
})
