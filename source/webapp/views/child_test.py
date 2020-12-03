import json

from django.shortcuts import get_object_or_404, redirect
from django.views import View
from django.views.generic import ListView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from webapp.context_for_test import ContextForTest
from webapp.models import Test, Child, Skill, SkillLevel


class TestsView(ListView):
    template_name = 'child/child_tests.html'
    model = Test
    paginate_by = 5
    paginate_orphans = 0

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        test = Test.objects.filter(child_id=self.kwargs.get('pk')).order_by('-id')
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


class ChildMakeTestView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        child = get_object_or_404(Child, pk=kwargs.get('pk'))
        test = Test.objects.create(child=child, therapist=self.request.user)
        query_tests = child.test.order_by('-created_date')
        if len(query_tests) > 1:
            previous_test = query_tests[1]
            test.previus_test = previous_test
            test.save()
        return redirect('webapp:child_update_test', pk=test.pk)


class ChildTestUpdateView(LoginRequiredMixin, TemplateView):
    template_name = 'child/child_make_test.html'
    model = Test
    paginate_by = 5
    paginate_orphans = 0

    def get_context_data(self, **kwargs):
        test = get_object_or_404(Test, pk=self.kwargs.get('pk'))
        context = super().get_context_data(**kwargs)
        category_cod = self.request.GET.get('ABC')
        context['skills'] = Skill.objects.filter(category__code=category_cod)
        context['child_pk'] = test.child.pk
        context['test'] = test
        context['ABC'] = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M',
                          'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
        return context

    def post(self, request, *args, **kwargs):
        test = get_object_or_404(Test, pk=self.kwargs.get('pk'))
        data = json.loads(request.body)
        skill_lvl = SkillLevel.objects.get(pk=data['id'])
        code = skill_lvl.skill.code

        for i in test.skill_level.all():
            if skill_lvl == i:
                test.skill_level.remove(i)
                test.save()
                return redirect('webapp:child_update_test', pk=test.pk)
            if code == i.skill.code:
                test.skill_level.remove(i)
        test.skill_level.add(skill_lvl)
        test.save()
        return redirect('webapp:child_update_test', pk=test.pk)
