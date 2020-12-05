from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.views.generic import DetailView, CreateView, UpdateView

from webapp.forms import ProgramForm
from webapp.models import Program, SKILL_STATUS_OPEN, PROGRAM_STATUS_CLOSED, PROGRAM_STATUS_OPEN, Child, ProgramSkill, \
    GOAL_STATUS_OPEN, ProrgamSkillGoal


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
        return reverse('webapp:program_detail', kwargs={'pk': program.pk})

