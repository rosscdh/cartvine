{% load url from future %}
//# ----- DATA STORE ----- #//
$(document).ready(function() {
    if (cartvine_is_ready) {

        var App = Em.Application.create();

        //# ----- DATA STORE ----- #//

        // App.store = DS.Store.create({
        //   revision: 4,
        //   adapter: DS.DjangoTastypieAdapter.create(),
        // });
        // App.store.adapter.set('serverDomain', url_scheme + '{{ request.get_host }}/');

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
        App.Product = Ember.Object.extend({
            url: 'products',
        });
        App.Shop = Ember.Object.extend({
            url: 'shops',
        });
        // App.Customer = DS.Model.extend({
        //     url: 'customers',
        // });
        Person = Ember.Object.extend({
            url: 'persons',
            FBUser: void 0,
            is_valid: void 0,
            shops: void 0,

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
        fb_login_title_view.appendTo('{{ config.target_id|default:"body" }}');
        fb_login_view.appendTo('{{ config.target_id|default:"body" }}');

        $('a#vine-fb-connect').live('click', function (e) {
            event.preventDefault();
            document.location = shoppers_url;
        });
    } // end cartvine_is_ready
});
