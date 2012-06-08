{% load url from future %}
//this.widget_prop_plus = function() {
this.{{ widget.widget_js_name }} = function() {
    var _this = this;

    this.App.productsView = Em.View.create({
      template: Em.Handlebars.compile("<h1>PROJECTS</h1><p>State: {{this.App.routeManager.currentState.path}}</p>")
    });
    this.App.cartView = Em.View.create({
      template: Em.Handlebars.compile("<h1>CART VIEW</h1><p>State: {{this.App.routeManager.currentState.path}}</p>")
    });

    this.App.routeManager = Em.RouteManager.create({
        products: Em.ViewState.create({
            route: 'products',
            enter: function(stateManager, transition) {
                console.log('Entered Ember products view')
            }
        }),
        cart: Em.ViewState.create({
            route: 'cart',
            enter: function(stateManager, transition) {
                console.log('Entered Ember cart view')
            }
        })
    });
},
