import json

from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect
from django.views import View
from django.views.generic import ListView, TemplateView

from webapp.models import Session, Child, Program, SkillLevel, SessionSkill


class SessionListView(ListView):
    template_name = 'session/session_list.html'
    context_object_name = 'session'
    paginate_by = 10
    paginate_orphans = 0
    model = Session

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        program = get_object_or_404(Program, pk=self.kwargs.get('pk'))
        sessions = Session.objects.filter(child=program.child.pk)
        context['sessions'] = sessions
        context['program'] = program
        return context



