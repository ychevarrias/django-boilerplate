from django.shortcuts import render
from django.views.generic import TemplateView

from apps.core.tasks import test_task


class HomeView(TemplateView):
    template_name = "index.html"


class TaskTestView(TemplateView):
    template_name = "index.html"

    def get_context_data(self, **kwargs):
        numbers_raw = self.request.GET.get("sum", "1,1")
        numbers = map(int, numbers_raw.split(","))
        async_task = test_task.apply_async(
            countdown=5, args=list(numbers)
        )
        kwargs["task_id"] = async_task.id
        return kwargs

