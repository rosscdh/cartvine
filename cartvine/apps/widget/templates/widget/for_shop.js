
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

    this.injectView = function(view, widget_name, target) {
    	target_ob = $(target);
	    if (target_ob.length <= 0 || target == 'body') {
	        // view insert target not found
			$('body').append(view);
	    }else{
            target_ob.append(view);
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

                    if (Davis != 'undefined') {
                        self.App = Davis(function () {});
                    }

                    if (loaded_widgets == num_widgets) {
                        self.loadWidgets();
                    }

	                if (xhr.status == 304) return;
	            },
	            error: function () {}
	        });

    	});
    }

    this.loadWidgets = function() {
        var self = this;
		// complete init
		{% spaceless %}{% for widget in widget_list_init_names %}
		//self.{{ widget }}();
		{% endfor %}{% endspaceless %}

        // Output of combined widgets
        {{ combined_widgets|safe }}
        // /End Output of combined widgets

        self.App.start();
    }
};

// cv instance
var cartvine = new CartVine();
cartvine.init();


