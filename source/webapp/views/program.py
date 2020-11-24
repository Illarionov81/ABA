from django.shortcuts import get_object_or_404
from django.views.generic import DetailView

from webapp.models import Program, SKILL_STATUS_OPEN, PROGRAM_STATUS_CLOSED, PROGRAM_STATUS_OPEN


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