{% load url from future %}
this.widget_prop_plus = function() {
    var _this = this;

    this.App.routeManager = Em.RouteManager.create({
        products: Em.ViewState.create({}),
        product: Em.ViewState.create({}),
        cart: Em.ViewState.create({}),
    });
},
