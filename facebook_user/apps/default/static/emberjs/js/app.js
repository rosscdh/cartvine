var App = Em.Application.create(Em.Facebook);
App.set('appId', '209234305864956');

//# ----- OVERRIDES & EXTENSIONS ----- #//

App.reopen({
    person: null,
    fBUserChanged: function() {
        var _this = this;

        this.person = Person.create({
            FBUser: this.FBUser
        });

    }.observes('FBUser')
});

//# ----- MODELS ----- #//
Person = Ember.Object.extend({
    FBUser: null,
    init: function() {
      this._super();
      this.validatePerson();
    },
    JsonifyFBUser: function() {
        return {
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
        }
    },
    /**
    Validate the Person specifed here, from facebook
    */
    validatePerson: function() {
        $.ajax({
                url: '/person/validate/',   // Hard Coded for now
                type: 'POST',
                data: this.JsonifyFBUser()
            })
            .done(function(data, textStatus, jqXHR) {
                console.log('Person Validation reponse: ' + textStatus);
            })
            .fail(function() { 
                console.log("error"); 
            });
            // .always(function() {
            // })
    }
});

//# ----- CONTROLLERS ----- #//


//# ----- VIEWS ----- #//
var fb_login_nav_view = Em.View.create({
  templateName: 'customer-nav',
});
var fb_login_title_view = Em.View.create({
  templateName: 'page-title',
});
var fb_login_view = Em.View.create({
  templateName: 'fb_login',
});