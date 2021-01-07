import json

from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from django.views.generic import DetailView, CreateView, DeleteView
from django.views.generic.base import View, TemplateView

from webapp.forms import ProgramForm
from webapp.models import Program, SKILL_STATUS_OPEN, PROGRAM_STATUS_CLOSED, PROGRAM_STATUS_OPEN, Child, ProgramSkill, \
    GOAL_STATUS_OPEN, ProrgamSkillGoal, Skill, SkillLevel


class ProgramDetailView(DetailView):
    template_name = 'program/program_detail_view.html'
    model = Program
    context_object_name = 'programs'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        program = get_object_or_404(Program, pk=self.kwargs.get('pk'))
        goals = ProrgamSkillGoal.objects.filter(skill__program=program)
        skill_open = program.program_skill.all().filter(status=SKILL_STATUS_OPEN)
        goal_open = goals.filter(status=GOAL_STATUS_OPEN)
        pr_skill = program.program_skill.all().order_by('-status', 'level')
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
        program = get_object_or_404(Program, pk=self.object.pk)
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
        prorgam_skill = ProgramSkill()
        if data['add_creteria']:
            prorgam_skill.add_creteria = data['add_creteria']
        prorgam_skill.level = skill_lvl
        prorgam_skill.program = program
        prorgam_skill.save()
        goals = data['goals']
        if goals:
            for g in goals:
                if g:
                    goal = ProrgamSkillGoal()
                    goal.skill = prorgam_skill
                    goal.goal = g
                    goal.save()
        else:
            goal = ProrgamSkillGoal()
            goal.save()

        return redirect('webapp:update_program', pk=program.pk)


class ProgrmDelete(DeleteView):
    template_name = 'program/delete_program.html'
    model = Program

    def get_success_url(self):
        return reverse('webapp:child_view', kwargs={'pk': self.object.child.pk})


class DeleteGoalView(DeleteView):
    # template_name = 'program/delete_goal.html'
    model = ProrgamSkillGoal

    def get(self, request, *args, **kwargs):
        return self.delete(request, *args, **kwargs)

    def get_success_url(self):
        return reverse('webapp:program_detail', kwargs={'pk': self.object.skill.program.pk})


class DeleteCreteriaView(DeleteView):
    template_name = 'program/program_detail_view.html'
    model = ProgramSkill

    def get(self, request, *args, **kwargs):
        return self.delete(request, *args, **kwargs)

    def get_success_url(self):
        return reverse('webapp:program_detail', kwargs={'pk': self.object.program.pk})


class DeleteAddCreteriaView(View):
    def get(self, request, *args, **kwargs):
        prskill = get_object_or_404(ProgramSkill, pk=self.kwargs.get('pk'))
        prskill.add_creteria = None
        self.prskill = prskill
        prskill.save()
        return self.get_success_url()

    def get_success_url(self):
        return redirect("webapp:program_detail", self.prskill.program.pk)

class RemoveProgramView(TemplateView):
    model = Program

    def get(self, request, *args, **kwargs):
        skill_lvl = SkillLevel.objects.get(pk=self.kwargs.get('s_pk'))
        p_pk = self.kwargs.get('p_pk')
        program_skill = skill_lvl.program_skill.all().filter(program__pk=p_pk)[0]
        goals = program_skill.goal.all()
        g = []
        for goal in goals:
            g.append(goal.goal)
        print(goals)
        responseData = {
            # 'criteria': skill_lvl.criteria,
            'add_creteria': program_skill.add_creteria,
            'goals': g or []
        }
        return HttpResponse(json.dumps(responseData), content_type="application/json")

    def post(self, request, *args, **kwargs):

        skill_lvl = SkillLevel.objects.get(pk=self.kwargs.get('s_pk'))
        p_pk = self.kwargs.get('p_pk')
        program_skill = skill_lvl.program_skill.all().filter(program__pk=p_pk)[0]
        program_skill.goal.all().delete()


        program = get_object_or_404(Program, pk=self.kwargs.get('p_pk'))
        data = json.loads(request.body)
        skill_lvl = SkillLevel.objects.get(pk=data['id'])

        if data['add_creteria'] and not program_skill:
            program_skill = ProgramSkill()
            program_skill.add_creteria = data['add_creteria']
            program_skill.level = skill_lvl
            program_skill.program = program
        elif not data['add_creteria'] and program_skill:
            program_skill.add_creteria = None
        else:
            program_skill.add_creteria = data['add_creteria']

        program_skill.save()

        goals = data['goals']
        if goals:
            for g in goals:
                if g:
                    goal = ProrgamSkillGoal()
                    goal.skill = program_skill
                    goal.goal = g
                    goal.save()
        else:
            goal = ProrgamSkillGoal()
            goal.save()

        return redirect('webapp:update_program', pk=program.pk)

class ExportWord(View):
    pass



