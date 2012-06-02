// CV object
var CartVine = function() {
    this.shop = "{{ object.name }}",
    this.cartvine_shop_id = "{{ object.pk }}",
    this.slug = "{{ object.slug }}",
    this.widgets = [{% for s in scripts %}"{{ s }}"{% if not forloop.last %},{% endif %}{% endfor %}],
    this.templates = [{% for t in templates %}"{{ t|escapejs }}"{% if not forloop.last %},{% endif %}{% endfor %}]
    this.App = void 0,
    this.DS = void 0,

    {{ combined_widgets|safe }}

    this.init = function () {
    	var _this = this

	    // Install Templates
	    $.each(this.templates, function(index) {
	        $(_this.templates[index]).appendTo('head');
	    });

    	// Install Scripts
    	// @TODO combine this
    	$.each(this.widgets, function(index) {
    		var url = _this.widgets[index];

    		$.ajaxSetup({ cache: true });

	        $.ajax({
	            url: url,
	            dataType: 'script',
	            cache: true,
	            complete: function(xhr) { 
	                if (typeof Em != 'undefined') {
	                    // Create the EmberJs Application which is shared between widgets
	                    // @TODO create object with event handlers to initialize CartVine objects
	                    _this.App = Em.Application.create();
	                };
	                if (typeof _this.App != 'undefined' && typeof DS != 'undefined' && typeof DS.DjangoTastypieAdapter != 'undefined') {
	                	_this.DS = DS;
	                    _this.App.store = DS.Store.create({
	                      revision: 4,
	                      adapter: DS.DjangoTastypieAdapter.create({
	                        serverDomain: url_scheme + "{{ request.get_host }}/",
	                        tastypieApiUrl: "api/v1/"
	                      })
	                    });
	                    _this.loadWidgets();
	                };
	                if (xhr.status == 304) return;
	            },
	            error: function () {}
	        });
    	});
		// fix local vars
		this.App = _this.App;
		this.DS = _this.DS;
    },
    this.loadWidgets = function() {
		// complete init @TODO find a way to make this dynamic
		{% for w in widget_list_init_names %}
		this.{{ w }}();
		{% endfor %}
    }
};

// cv instance
var cartvine = new CartVine();
cartvine.init();