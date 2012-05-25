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
        $.ajax({
            url: '/person/validate/',   // Hard Coded for now
            type: 'POST',
            data: {'person': this.FBUser }
        })
            .done(function(data) {
                console.log(_this.person.say())
            })
            .fail(function() { alert("error"); })
            .always(function() {});
    }.observes('FBUser')
});

//# ----- MODELS ----- #//
Person = Ember.Object.extend({
    FBUser: null,
    say: function() {
    console.log(this.FBUser.picture)
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