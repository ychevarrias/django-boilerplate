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
