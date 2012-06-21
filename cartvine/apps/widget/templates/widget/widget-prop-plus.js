{% load url from future %}
this.{{ widget.widget_js_name }} = function() {
    var self = this;


    var app = Sammy('#main', function() {
      // include a plugin


      // define a 'route'
      this.get('#/products/(.*)', function() {
        // load some data
        alert('fdasd')
      });
    });

    // start the application
    app.run('#/products');

    var variationControls = function() {
        var source   = $("script#variation-controls").html();
        var context = {
        };
        var template = Handlebars.compile(source);
        return template(context);
    };

    self.injectView(variationControls(), '{{ widget.widget_js_name }}', '{{ config.variations.target_id }}');

}
