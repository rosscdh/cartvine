var App = Em.Application.create(Em.Facebook);
App.set('appId', '209234305864956');

//# ----- MODELS ----- #//


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