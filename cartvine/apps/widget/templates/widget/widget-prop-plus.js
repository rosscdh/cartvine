{% load url from future %}
//this.widget_prop_plus = function() {
this.{{ widget.widget_js_name }} = function() {
    var _this = this;

    this.App.productsView = Em.View.create({
      template: Em.Handlebars.compile("<h1>PROJECTS</h1><p>State: {{this.App.routeManager.currentState.path}}</p>")
    });

    this.App.routeManager = Em.RouteManager.create({
        products: Em.ViewState.create({}),
        projects: Em.ViewState.create({
        route: 'products',
        view: this.App.productsView
        }),
        cart: Em.ViewState.create({}),
    });
},
