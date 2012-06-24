//$(document).ready(function () {
    // CV object
    var CartVine = function() {
        var self = this;

        this.App = void 0,
        this.url_scheme = window.parent.document.location.protocol + '//',
        this.shop = "{{ object.name }}",
        this.shop_url = "{{ object.url }}",
        this.cartvine_shop_id = "{{ object.pk }}",
        this.slug = "{{ object.slug }}",
        this.widgets = [{% for s in scripts %}"{{ s }}"{% if not forloop.last %},{% endif %}{% endfor %}],
        this.templates = [{% for t in templates %}"{{ t|escapejs }}"{% if not forloop.last %},{% endif %}{% endfor %}]

        this.buildUrl = function (path) {
            if (path.substr(0,1) == '/') {
                path = path.substr(1);
            }
            url = self.url_scheme + '{{ cartvine_sites.shopify_app_domain }}/';
            request_url = url + path;
            return request_url;
        }

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
                var template = $.trim(self.templates[index]);
                if (template.length > 0) {
                   $('head').append(template);
                }
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
            if (Davis != 'undefined') {

                self.App = Davis(function () {
                    var d = this;

                    // Start app Url
                    {{ combined_widgets|safe }}

                });

                self.App.start();
            };
        }
    };

    // cv instance
    var cartvine = new CartVine();
    cartvine.init();


//});
