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
        productController = Em.ArrayController.create({
          content: App.store.findAll(App.Product),

          selectedProduct: undefined,

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
        // productsView = Ember.CollectionView.create({
        //   tagName: 'ul',
        //   classNames: ['a-collection'],
        //   content: [productController.content[0].name],
        //   itemViewClass: Ember.View.extend({
        //     template: Ember.Handlebars.compile("{{content}}")
        //   })
        // })
        productsView = Em.View.create({
          products: productController.content,
          templateName: '{{ object.slug }}-product_list'
        });
        // productsView = Em.CollectionView.create({
        //   contentBinding: 'App.productController.content',
        //   tagName: "ul",

        //   //NOTE Formerly known as itemView
        //   itemViewClass: Em.View.extend({
        //     classNames: ['product'],
        //     template: '{{ object.slug }}-product_list',
        //   })
        // });

        //# ----- INSTANTIATE VIEWS ----- #//
        productsView.appendTo('{{ config.target_id|default:"body" }}');

        //# ----- HELPER JS ----- #//
        $('a#vine-fb-connect').live('click', function (e) {});
    } // end cartvine_is_ready
});
