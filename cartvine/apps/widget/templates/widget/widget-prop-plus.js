{% load url from future %}
this.{{ widget.widget_js_name }} = function() {
    var self = this;

    self.variationControls = function() {
        var source   = $("script#variation-controls").html();
        var template = Handlebars.compile(source);
        var context = {
            'properties_list': ['a','b','c'],
            'variations_list': ['1','2','3']
        }
        return template(context);
    };
    
    self.productProperties = function() {
        var source   = $("script#product-properties").html();
        var template = Handlebars.compile(source);
        var context = {
            'properties_list': [
                {'name': 'Name goes here', 'value': 'Value goes here'},
            ],
        }
        return template(context);
    };

    this.injectView(self.variationControls(), '{{ widget.widget_js_name }}', '{{ config.variations.target_id }}');
    this.injectView(self.productProperties(), '{{ widget.widget_js_name }}', '{{ config.properties.target_id }}');
},
