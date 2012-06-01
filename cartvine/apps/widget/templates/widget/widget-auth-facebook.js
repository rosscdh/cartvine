{% load url from future %}
//# ----- DATA STORE ----- #//
$(document).ready(function() {
    if (cartvine_is_ready) {
        //# ----- APP OVERRIDES & EXTENSIONS ----- #//
        App.reopen({
            fBUserChanged: function() {
                var _this = this;

                this.set('Person', Person.create({
                    FBUser: this.FBUser
                }));

            }.observes('FBUser')
        });

        //# ----- MODELS ----- #//
        App.Person = DS.Model.extend({
            url: 'persons',

            access_token: DS.attr('string')
            //data: DS.attr('string')
        });

        //# ----- CONTROLLERS ----- #//

        //# ----- VIEWS ----- #//
        var fb_login_view = Em.View.create({
          templateName: '{{ object.slug }}-fb_login',
        });

        //# ----- INSTANTIATE VIEWS ----- #//
        fb_login_view.appendTo('{{ config.target_id|default:"body" }}');

        //# ----- HELPER JS ----- #//
        $('a#vine-fb-connect').live('click', function (e) {
            event.preventDefault();
            window.open(shoppers_url, "{{ object.slug }}-window", "width=640, height=480");
            return false;
        });
    } // end cartvine_is_ready
});
