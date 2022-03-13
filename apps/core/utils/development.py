from django.http import JsonResponse
from django.shortcuts import render
from django.views.generic import TemplateView


class TemplateRender(TemplateView):

    def get_template_names(self):
        path = self.request.path
        if path == '/':
            path = "index.html"
        return [f"maqueta/{path}"]

    def post(self):
        return JsonResponse({}, status=200)


def front_context(request):
    def looper(length):
        for loop in range(length):
            yield loop
    _loops = [
        2, 4, 6, 8, 10, 12, 16, 32, 64,
        3, 5, 7, 9, 11, 13, 15, 25, 50,
    ]
    context = dict()
    for loop in _loops:
        context[f"looper_{loop}"] = looper(loop)
    return context
