var App = Em.Application.create(Em.Facebook);
App.set('appId', '209234305864956');

App.MyView = Em.View.extend({
  mouseDown: function() {
    window.alert("hello world!");
  }
});

var fb_login_view = Em.View.create({
  templateName: 'fb_login',
  name: "Bob"
});