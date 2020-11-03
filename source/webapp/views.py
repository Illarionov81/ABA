from django.shortcuts import render
from django.views.generic import DetailView, ListView
from webapp.models import Child, TestResult, Test


class ChildDetailView(DetailView):
    template_name = 'child/child_view.html'
    model = Child


class ChildTestsView(ListView):
    template_name = 'child/child_tests.html'
    model = Test
    ordering = ['-edited_date']
    paginate_by = 5
    paginate_orphans = 0

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        test = Test.objects.filter(child_id=self.kwargs.get('pk'))
        context['Test'] = test
        return context
