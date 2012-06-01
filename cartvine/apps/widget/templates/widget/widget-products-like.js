{% load url from future %}
//# ----- DATA STORE ----- #//
$(document).ready(function() {
    if (cartvine_is_ready) {
        //# ----- APP OVERRIDES & EXTENSIONS ----- #//

        //# ----- MODELS ----- #//
        App.Product = DS.Model.extend({
            //url: 'product',
            name: DS.attr('string'),
            slug: DS.attr('string')
        });

        //# ----- CONTROLLERS ----- #//
        /**
         * The main application controller. Provides an interface
         * for the views to interact with the models
         */
        App.productController = Em.ArrayController.create({
          content: App.store.findAll(App.Product),
          //content: null,

          selectedProduct: undefined,

          noEditable: Em.computed(function(){
            return (this.get('selectedProduct') === undefined);
          }).property('selectedProduct'),

          getProduct: function(name){
            for(var i=0;i<this.content.length;i++){
              if (name===this.content.get(i).name){
                return this.content.get(i);
              }
            }
            return null;
          },

          saveChanges: function(){
            //App.store.commit();
          }
        });


        //# ----- VIEWS ----- #//
        /**
         * The list of products
         */
        App.ProductsView = Em.CollectionView.extend({
          contentBinding: 'App.productController.content',
          tagName: "ul",

          //NOTE Formerly known as itemView
          itemViewClass: Em.View.extend({
            classNames: ['product'],
            // selected: Em.computed(function(){
            // }).property('parentView.selectedProduct'),
            template: Em.Handlebars.compile('{{ object.slug }}-products_like_this_one'),
            mouseDown: function(evt) {
            }
          })
        });

        //# ----- INSTANTIATE VIEWS ----- #//
        productsView = App.ProductsView.create({});
        productsView.appendTo('{{ config.target_id|default:"body" }}');

        //# ----- HELPER JS ----- #//
        $('a#vine-fb-connect').live('click', function (e) {});
    } // end cartvine_is_ready
});
