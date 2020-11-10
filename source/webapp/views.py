from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, get_object_or_404
from django.views.generic import DetailView, ListView
from webapp.models import Child, Test, Skill


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

    # def get_context_data(self, *, object_list=None, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     test = Test.objects.get(pk=self.kwargs.get('pk'))
    #     result = TestResult.objects.filter(test_id=test.pk).order_by('test')
    #     if test.previus_test:
    #         previous_test = Test.objects.get(pk=test.previus_test.pk)
    #         previous_result = TestResult.objects.filter(test_id=previous_test.pk)
    #         context['Previous_result'] = previous_result
    #         context['previous_test'] = previous_test
    #         previous_test_result = []
    #         diff = []
    #         for i in previous_result:
    #             previous_test_result.append(i.skill_level.skill.code)
    #         print(previous_test_result)
    #         for i in result:
    #             if i.skill_level.skill.code in previous_test_result:
    #                 pass
    #             else:
    #                 diff.append(i)
    #         context['diff'] = diff
    #     child = test.child
    #     context['child'] = child
    #     context['Result'] = result
    #     context['test'] = test
    #     return context
#
