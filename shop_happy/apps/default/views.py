from django.views.generic.base import TemplateView


class DefaultView(TemplateView):
    template_name = 'default/default.html'

    def get(self, request, *args, **kwargs):
        context = []
        return self.render_to_response(context)
