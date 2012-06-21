
// CV object
var CartVine = function() {
    var self = this;

    this.shop = "{{ object.name }}",
    this.shop_url = "{{ object.url }}",
    this.cartvine_shop_id = "{{ object.pk }}",
    this.slug = "{{ object.slug }}",
    this.widgets = [{% for s in scripts %}"{{ s }}"{% if not forloop.last %},{% endif %}{% endfor %}],
    this.templates = [{% for t in templates %}"{{ t|escapejs }}"{% if not forloop.last %},{% endif %}{% endfor %}]
    this.App = void 0,
    this.DS = void 0,

    // Output of combined widgets
    {{ combined_widgets|safe }}
    // /End Output of combined widgets

    this.injectView = function(view, widget_name, target) {
    	target_ob = $(target);
	    if (target_ob.length <= 0 || target == 'body') {
	        // view insert target not found
	        //$('body').append('<p><strong>Please Note:</strong> You have specified ('+ target +') to insert this the "'+ widget_name +'" widget into, but it does not exist.</p>')
	        if (typeof DS != 'undefined') {
	            view.appendTo('body');
            }else{
			    $('body').append(view);
		    }
			
	    }else{
	        if (typeof DS != 'undefined') {
	            // ember
                view.appendTo(target_ob);
	        }else{
	            // straight jquery
	            target_ob.append(view);  
	        }
	    }
    }

    this.init = function () {
    	var self = this;

	    // Install Templates
	    $.each(this.templates, function(index) {
	        $('head').append($(self.templates[index]));
	    });

    	// Install Scripts
    	// @TODO combine this
    	var num_widgets = this.widgets.length;
    	var loaded_widgets = 0;
    	$.each(this.widgets, function(index) {
    		var url = self.widgets[index];

    		$.ajaxSetup({ cache: true });

	        $.ajax({
	            url: url,
	            dataType: 'script',
	            cache: true,
	            complete: function(xhr) { 
	                loaded_widgets++;

                    if (typeof Em != 'undefined') {
                        // Create the EmberJs Application which is shared between widgets
                        // @TODO create object with event handlers to initialize CartVine objects
                        self.App = Em.Application.create();
                    };

                    if (typeof self.App != 'undefined' && typeof DS != 'undefined' && typeof DS.DjangoTastypieAdapter != 'undefined') {
                        self.DS = DS;
                        self.App.store = DS.Store.create({
                                revision: 4,
                                    adapter: DS.DjangoTastypieAdapter.create({
                                    serverDomain: url_scheme + "{{ request.get_host }}/",
                                    tastypieApiUrl: "api/v1/"
                                })
                        });
                    };

                    // Routing
                    if (typeof self.App != 'undefined') {
                        self.App.routeManager = Em.RouteManager.create({});
                    }

                    if (loaded_widgets == num_widgets) {
                        self.loadWidgets();
                    }

	                if (xhr.status == 304) return;
	            },
	            error: function () {}
	        });

    	});
		// fix local vars
		this.App = self.App;
		this.DS = self.DS;
    }

    this.loadWidgets = function() {
        // fire the route manager event to bind the current page with the established routes (ember lame)
        self.App.routeManager.set('location', window.location.pathname);

		// complete init
		{% spaceless %}{% for widget in widget_list_init_names %}
		this.{{ widget }}();
		{% endfor %}{% endspaceless %}
    }
};

// cv instance
var cartvine = new CartVine();
cartvine.init();
