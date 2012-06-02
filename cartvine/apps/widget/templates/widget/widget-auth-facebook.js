{% load url from future %}
this.widget_auth_facebook = function() {
    //# ----- WIDGET START {{ object.slug }} ----- #//
    //# ----- APP OVERRIDES & EXTENSIONS ----- #//
    //# ----- MODELS ----- #//
    this.App.Person = this.DS.Model.extend({
        url: 'persons',
        access_token: this.DS.attr('string')
        //data: DS.attr('string')
    });
    //# ----- CONTROLLERS ----- #//
    //# ----- VIEWS ----- #//
    var fb_login_view = Em.View.create({
      templateName: 'widget-auth-facebook-fb_login',
    });

    //# ----- INSTANTIATE VIEWS ----- #//
    fb_login_view.appendTo('{{ config.target_id|default:"body" }}');

    //# ----- HELPER JS ----- #//
    $('a#vine-fb-connect').live('click', function (e) {
        event.preventDefault();
        window.open(shoppers_url, "widget-auth-facebook-window", "width=640, height=480");
        return false;
    });
    //# ----- WIDGET END {{ object.slug }} ----- #//
},