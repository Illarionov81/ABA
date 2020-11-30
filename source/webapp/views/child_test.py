from django.shortcuts import get_object_or_404
from django.views.generic import ListView

from webapp.context_for_test import ContextForTest
from webapp.models import Test


class TestsView(ListView):
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
        checkbox = self.request.GET.get('checkbox')
        c = ContextForTest()
        data = c.all_test(test_pk, category_cod=category_cod, checkbox=checkbox)
        all_filtered_skill_code = data
        context['all_filtered_skill_code'] = all_filtered_skill_code
        return context
