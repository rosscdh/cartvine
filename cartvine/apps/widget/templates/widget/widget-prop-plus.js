{% load url from future %}
//this.{{ widget.widget_js_name }} = function() {

Davis.greeter = function () {
    this.get('/greet/:name', function (req) {
    alert("Hello " + req.params['name'])
    })
}


//}
