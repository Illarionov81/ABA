import json

from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from django.views.generic import DetailView, CreateView, UpdateView
from django.views.generic.base import View, TemplateView

from webapp.forms import ProgramForm
from webapp.models import Program, SKILL_STATUS_OPEN, PROGRAM_STATUS_CLOSED, PROGRAM_STATUS_OPEN, Child, ProgramSkill, \
    GOAL_STATUS_OPEN, ProrgamSkillGoal, Test, Skill, SkillLevel


class ProgramDetailView(DetailView):
    template_name = 'program/program_detail_view.html'
    model = Program
    context_object_name = 'programs'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        program = get_object_or_404(Program, pk=self.kwargs.get('pk'))
        goals = ProrgamSkillGoal.objects.filter(skill__program=program)
        skill_open = program.program_skill.all().filter(status=SKILL_STATUS_OPEN)
        print(goals)
        goal_open = goals.filter(status=GOAL_STATUS_OPEN)
        pr_skill = program.program_skill.all().order_by('-status', 'level')
        print(goal_open)
        print(skill_open)
        if not skill_open and not goal_open:
            program.status = PROGRAM_STATUS_CLOSED
        else:
            program.status = PROGRAM_STATUS_OPEN
        program.save()
        context['skills'] = pr_skill
        return context


class ProgramCreateView(CreateView):
    model = Program
    template_name = 'program/program_create.html'
    form_class = ProgramForm


    def form_valid(self, form):
        child = get_object_or_404(Child, pk=self.kwargs.get('pk'))
        program = form.save(commit=False)
        program.child = child
        form.instance.author = self.request.user
        program.save()
        return super().form_valid(form)

    def get_success_url(self):
        child = get_object_or_404(Child, pk=self.kwargs.get('pk'))
        program = get_object_or_404(Program, pk=child.programs.last().pk)
        return reverse('webapp:update_program', kwargs={'pk': program.pk})


class UpdateProgram(TemplateView):
    template_name = 'program/program_add_skill.html'
    model = Program

    def get_context_data(self, **kwargs):
        program = get_object_or_404(Program, pk=self.kwargs.get('pk'))
        child = program.child
        test = child.test.last()
        context = super().get_context_data(**kwargs)
        if test:
            category_cod = self.request.GET.get('ABC')
            context['skills'] = Skill.objects.filter(category__code=category_cod)
            context['child_pk'] = test.child.pk
            context['program'] = program
            context['test'] = test
            context['ABC'] = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M',
                              'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']

        else:
            context['error'] = 'Нет ни одного проведенного теста'
        return context

    def post(self, request, *args, **kwargs):
        program = get_object_or_404(Program, pk=self.kwargs.get('pk'))
        data = json.loads(request.body)
        skill_lvl = SkillLevel.objects.get(pk=data['id'])
        program.skills.add(skill_lvl)
        return redirect('webapp:update_program', pk=program.pk)
        # code = skill_lvl.skill.code


        # for i in program.program_skill.all():
        #     if skill_lvl == i:
        #         program.program_skill.remove(i)
        #         program.save()
        #         return redirect('webapp:update_program', pk=program.pk)
        #     if code == i.skill.code:
        #         program.program_skill.remove(i)
        # program.program_skill.add(skill_lvl)
        # program.save()

