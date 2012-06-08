{% load url from future %}
this.widget_prop_plus = function() {
    var _this = this;
    //# ----- WIDGET START {{ object.slug }} ----- #//
    this.App.routeManager = Em.RouteManager.create({
      projects: Em.ViewState.create({
        route: 'cart',
        enter: function(stateManager, transition) {
          this._super(stateManager, transition);
          var params = stateManager.get('params');
          alert(params)
          // do something here with postId
        }
      },
      projects: Em.ViewState.create({
        route: 'cart',
        enter: function(stateManager, transition) {
          this._super(stateManager, transition);
          var params = stateManager.get('params');
          alert(params)
          // do something here with postId
        }
      });
    //# ----- DATA STORE ----- #//
    //# ----- APP OVERRIDES & EXTENSIONS ----- #//
    //# ----- MODELS ----- #//
    this.App.Product = this.DS.Model.extend({
        shop_url: this.shop_url,
        vendor_id: this.DS.attr('number'),
        name: this.DS.attr('string'),
        slug: this.DS.attr('string'),
        featured_image: this.DS.attr('string'),
        tags: this.DS.attr('string'),
        vendor: this.DS.attr('string'),
    });

    //# ----- CONTROLLERS ----- #//
    //# ----- VIEWS ----- #//
    /**
     * The list of products
     */
     productsView = Em.View.create({
        products: _this.App.store.findAll(_this.App.Product),
        templateName: 'cartvine-products_like_this_one',
     });
    //# ----- INSTANTIATE VIEWS ----- #//

    this.injectView(productsView, 'widget_products_like', '{{ config.target_id }}');

    //# ----- HELPER JS ----- #//
    $('a#vine-fb-connect').live('click', function (e) {});

    //# ----- WIDGET END {{ object.slug }} ----- #//
},
