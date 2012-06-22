{% load url from future %}
this.{{ widget.widget_js_name }} = function() {
    var self = this;
    var app = Sammy('#main', function() {

        // define a 'route'
        this.get('/products/:slug', function() {
            var sam = this;

            self.App.Product = self.DS.Model.extend({
                id: DS.attr('number'),
                slug: DS.attr('string'),
                name: DS.attr('string'),
                prop_list: function() {
                    return [{'option_id':'option1', 'name':'My First Property',}];
                }.property()
            });

            var variationControlsView = function(sam) {
                var slug = sam.params.slug.replace('.html', '');
                var source   = $("script#variation-controls").html();

                var Product = self.App.store.find(self.App.Product, {'slug': slug});
                console.log(Product)
                var context = {
                    'product': Product,

                };
                var template = Handlebars.compile(source);
                return template(context);
            };

            self.injectView(variationControlsView(sam), '{{ widget.widget_js_name }}', '{{ config.variations.target_id }}');

            });
        });

    // start the application
    app.run('#/');
}
