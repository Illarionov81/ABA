from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, get_object_or_404
from django.views.generic import DetailView, ListView, CreateView
from webapp.models import Child, Test, Skill, Program, SkillLevel, ProgramSkill, PROGRAM_STATUS_CLOSED, \
    SKILL_STATUS_OPEN, PROGRAM_STATUS_OPEN, SKILL_STATUS_CLOSED
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

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        program = Program.objects.filter(child=self.kwargs.get('pk'))
        context['programs'] = program
        return context


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
        checkbox = self.request.GET.get('checkbox')
        c = ContextForTest()
        data = c.all_test(test_pk, category_cod=category_cod, checkbox=checkbox)
        all_filtered_skill_code = data
        context['all_filtered_skill_code'] = all_filtered_skill_code
        return context


class ProgramDetailView(DetailView):
    template_name = 'program/program_detail_view.html'
    model = Program
    context_object_name = 'programs'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        program = get_object_or_404(Program, pk=self.kwargs.get('pk'))
        pr_skill = program.program_skill.all().order_by('-status', 'level')
        skill_open = program.program_skill.all().filter(status=SKILL_STATUS_OPEN)
        if not skill_open:
            program.status = PROGRAM_STATUS_CLOSED
        else:
            program.status = PROGRAM_STATUS_OPEN
        program.save()
        context['skills'] = pr_skill
        return context












