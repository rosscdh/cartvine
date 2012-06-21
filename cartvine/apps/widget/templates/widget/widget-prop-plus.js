{% load url from future %}
this.{{ widget.widget_js_name }} = function() {
    var self = this;

    // ----- MODELS -----
    self.App.Variant = self.DS.Model.extend({
        id: self.DS.attr('number'),
        title: self.DS.attr('string'),
        slug: self.DS.attr('string'),
        sku: self.DS.attr('string'),
        compare_at_price: self.DS.attr('string'),
        fulfillment_service: self.DS.attr('string'),
        grams: self.DS.attr('string'),
        inventory_management: self.DS.attr('boolean'),
        inventory_policy: self.DS.attr('string'),
        inventory_quantity: self.DS.attr('number'),
        option1: self.DS.attr('string'),
        option2: self.DS.attr('string'),
        option3: self.DS.attr('string'),
        position: self.DS.attr('number'),
        price: self.DS.attr('number'),
        product: self.DS.attr('string'),
        provider_id: self.DS.attr('string'),
        requires_shipping: self.DS.attr('boolean'),
        resource_uri: self.DS.attr('string'),
        taxable: self.DS.attr('string'),
        created_at: self.DS.attr('date'),
        updated_at: self.DS.attr('date')
    });


    // ----- VIEWS -----
    var variant_list = self.App.store.filter(self.App.Variant, function(data) {
        if (data.provider_id == 219102044) { return true; }
    });

    var variationControls = Ember.View.create({
      templateName: 'variation-controls',
      'variant_list': variant_list
    });
    var productProperties = Ember.View.create({
        templateName: 'product-properties',
        properties_list: [{'name': 'name 1', 'value': 'value 1'},{'name': 'name 2', 'value': 'value 2'},]
    });

    var variationControls = Ember.View.create({
      templateName: 'variation-controls',
      'variant_list': variant_list
    });

    this.injectView(variationControls, '{{ widget.widget_js_name }}', '{{ config.variations.target_id }}');
    this.injectView(productProperties, '{{ widget.widget_js_name }}', '{{ config.properties.target_id }}');
},
