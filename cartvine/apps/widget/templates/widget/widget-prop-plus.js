{% load url from future %}
this.{{ widget.widget_js_name }} = function() {
    var self = this;

    var Product = null;
    var Variant = null;

    var app = Sammy('#main', function() {

        // define a 'route'
        this.get('/products/:slug', function() {
            var sam = this;
            var slug = sam.params.slug.replace('.html', '');
            
            var url = 'http://{{ cartvine_sites.shopify_app_domain }}/api/v1/product/?slug=' + slug;
            $.getJSON(url, function(data) {
                self.Product = data.objects[0];

                var variationControlsView = function(sam) {
                    var source   = $("script#variation-controls").html();
                    var context = {
                        'product': self.Product,
                    };
                    var template = Handlebars.compile(source);
                    return template(context);
                };

                self.injectView(variationControlsView(), '{{ widget.widget_js_name }}', '{{ config.variations.target_id }}');

                var url = 'http://{{ cartvine_sites.shopify_app_domain }}/api/v1/variant/?product=' + self.Product.id;
                $.getJSON(url, function(data) {
                    self.Variant = data.objects[0];

                    var productPropertiesView = function(sam) {
                        var source   = $("script#product-properties").html();
                        var context = {
                            'product': self.Product,
                            'variant': self.Variant,
                        };
                        var template = Handlebars.compile(source);
                        return template(context);
                    };

                    self.injectView(productPropertiesView(), '{{ widget.widget_js_name }}', '{{ config.products.target_id }}');
                });
            });

            // var variationControlsView = function(sam) {
            //     var slug = sam.params.slug.replace('.html', '');
            //     var source   = $("script#variation-controls").html();


            //     var context = {
            //         'product': Product,

            //     };
            //     var template = Handlebars.compile(source);
            //     return template(context);
            // };

            // self.injectView(variationControlsView(sam), '{{ widget.widget_js_name }}', '{{ config.variations.target_id }}');

            });
        });

    // start the application
    app.run('#/');
}
