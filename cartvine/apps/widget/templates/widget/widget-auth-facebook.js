{% load url from future %}
//# ----- DATA STORE ----- #//
$(document).ready(function() {

    var App = Em.Application.create();
    App.set('appId', '{{ FACEBOOK_APP_ID }}');

    //# ----- DATA STORE ----- #//

    App.store = DS.Store.create({
      revision: 4,
      adapter: DS.DjangoTastypieAdapter.create(),
    });
    App.store.adapter.set('serverDomain', '{{ request.build_absolute_uri }}');

    //# ----- OVERRIDES & EXTENSIONS ----- #//

    App.reopen({
        Person: void 0,
        fBUserChanged: function() {
            var _this = this;

            this.set('Person', Person.create({
                FBUser: this.FBUser
            }));

        }.observes('FBUser')
    });

    //# ----- MODELS ----- #//
    App.Product = DS.Model.extend({
        url: 'products',
    });
    App.Shop = DS.Model.extend({
        url: 'shops',
        slug: DS.attr('string'),
        data: DS.attr('string'),
        shopify_id: DS.attr('string')
    });
    // App.Customer = DS.Model.extend({
    //     url: 'customers',
    // });
    Person = DS.Model.extend({
        url: 'persons',
        FBUser: void 0,
        is_valid: void 0,
        shops: void 0,
        products: DS.hasMany('App.Product'),

        init: function() {
            this._super();
            this.validatePerson();
        },

        isValidChanged: function() {
        }.observes('is_valid'),


        /**
        Convert the DBUser object into an dict that can be posted
        */
        JsonifyFBUser: function() {
            return JSON.stringify({
                'uid': this.FBUser.id,
                'access_token': this.FBUser.accessToken,
                'email': this.FBUser.email,
                'username': this.FBUser.username,
                'verified': this.FBUser.verified,
                'first_name': this.FBUser.first_name,
                'last_name': this.FBUser.last_name,
                'gender': this.FBUser.gender,
                'link': this.FBUser.link,
                'picture': this.FBUser.picture,
                'location': this.FBUser.location,
                'locale': this.FBUser.locale,
                'quotes': this.FBUser.quotes
            })
        },
        /**
        Validate the Person specifed here, from facebook
        */
        validatePerson: function() {
            var _this = this;
            $.ajax({
                    url: '/person/validate/facebook/',   // Hard Coded for now
                    type: 'POST',
                    contentType: 'application/json',
                    data: this.JsonifyFBUser()
                })
                .done(function(data, textStatus, jqXHR) {
                    _this.set('is_valid', data.is_valid);

                    if (data.is_valid) {
                        // _this.set('shops', data.shops);
                        // _this.set('products', data.products);
                    }
                })
                .fail(function() { 
                    console.log("error"); 
                })
                .always(function() {
                });
        },
        getShopProducts: function(shop_id) {
            console.log(shop_id)
            return []
        }
    });

    //# ----- CONTROLLERS ----- #//
    App.personProfileController = Em.Object.create({
    });


    //# ----- VIEWS ----- #//
    var fb_login_title_view = Em.View.create({
      templateName: 'widget-auth-facebook-title',
    });
    var fb_login_view = Em.View.create({
      templateName: 'widget-auth-facebook-fb_login',
    });


    //# ----- VIEWS ----- #//
    fb_login_title_view.appendTo('body');
    fb_login_view.appendTo('body'); 
});
