{% load url from future %}
this.productsLike = function() {
    //# ----- WIDGET START {{ object.slug }} ----- #//
    //# ----- DATA STORE ----- #//
    //# ----- APP OVERRIDES & EXTENSIONS ----- #//
    //# ----- MODELS ----- #//
    this.App.Product = DS.Model.extend({
        vendor_id: DS.attr('number'),
        name: DS.attr('string'),
        slug: DS.attr('string'),
        featured_image: DS.attr('string'),
        tags: DS.attr('string'),
        vendor: DS.attr('string'),
    });

    //# ----- CONTROLLERS ----- #//
    //# ----- VIEWS ----- #//
    /**
     * The list of products
     */
     productsView = Em.View.create({
        products: this.App.store.findAll(this.App.Product),
        templateName: '{{ object.slug }}-products_like_this_one',
     });
    //# ----- INSTANTIATE VIEWS ----- #//
    productsView.appendTo('{{ config.target_id|default:"body" }}');

    //# ----- HELPER JS ----- #//
    $('a#vine-fb-connect').live('click', function (e) {});

    //# ----- WIDGET END {{ object.slug }} ----- #//
},