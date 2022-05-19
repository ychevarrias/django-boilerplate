from django.shortcuts import render
from django.views.generic import TemplateView

from apps.core.tasks import test_task


class HomeView(TemplateView):
    template_name = "index.html"


class TaskTestView(TemplateView):
    template_name = "index.html"

    def get_context_data(self, **kwargs):
        async_task = test_task.delay()
        kwargs["task_id"] = async_task.id
        return kwargs

