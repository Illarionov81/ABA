from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, get_object_or_404
from django.views.generic import DetailView, ListView
from webapp.models import Child, Test, Skill
from webapp.context_for_test import ContextForTest


class IndexView(ListView):
    template_name = 'index.html'
    context_object_name = 'child'
    paginate_by = 5
    paginate_orphans = 0
    model = Child

    #    def get_queryset(self):
    #    data = super().get_queryset()
    #    if not self.request.GET.get('is_admin', None):
    #    data = data.filter(status='moderated')
    #    return data

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class ChildDetailView(DetailView):
    template_name = 'child/child_view.html'
    model = Child


class ChildTestsView(ListView):
    template_name = 'child/child_tests.html'
    model = Test
    paginate_by = 5
    paginate_orphans = 0

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        test = Test.objects.filter(child_id=self.kwargs.get('pk'))
        context['Test'] = test
        context['child_pk'] = self.kwargs.get('pk')
        return context


class TestResultView(ListView):
    template_name = 'child/test_result.html'
    model = Test
    paginate_by = 5
    paginate_orphans = 0

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        test = get_object_or_404(Test, pk=self.kwargs.get('pk'))
        context['test'] = test
        context['ABC'] = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M',
                          'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
        test_pk = test.pk
        category_cod = self.request.GET.get('ABC')
        c = ContextForTest()
        data = c.all_test(test_pk, category_cod=category_cod)
        tests, this_test, diff = data
        context['tests'] = tests
        context['this_test'] = this_test
        context['diff'] = diff
        return context

