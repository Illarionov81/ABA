import json
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from django.views import View
from django.views.generic import ListView, TemplateView, DeleteView
from webapp.models import Session, Program, ProrgamSkillGoal, SessionSkill


class SessionListView(ListView):
    template_name = 'session/session_list.html'
    context_object_name = 'session'
    paginate_by = 10
    paginate_orphans = 0
    model = Session

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        program = get_object_or_404(Program, pk=self.kwargs.get('pk'))
        sessions = Session.objects.filter(program=program)
        context['sessions'] = sessions
        context['program'] = program
        return context


class SessionDeleteView(DeleteView):
    template_name = 'session/session_delete.html'
    model = Session

    def get_success_url(self):
        return reverse('webapp:session_list', kwargs={'pk': self.object.program.pk})


class SessionCreateView(View):
    def get(self, request, *args, **kwargs):
        program = get_object_or_404(Program, pk=kwargs.get('pk'))
        sessions = Session.objects.filter(program=program).last()
        if sessions and sessions.status == 'open':
            return redirect('webapp:session_prepear', pk=sessions.pk)
        else:
            session = Session.objects.create(program=program, child=program.child, therapist=self.request.user)
            return redirect('webapp:session_prepear', pk=session.pk)


class SessionSkillUpdateView(TemplateView):
    template_name = 'session/session_create.html'
    model = Session

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        session = get_object_or_404(Session, pk=self.kwargs.get('pk'))
        goal = ProrgamSkillGoal.objects.filter(skill__program=session.program.pk)
        goal_in_session = SessionSkill.objects.filter(session=session).values_list('skill', flat=True)
        context['goal_in_session'] = goal_in_session
        context['goals'] = goal
        context['sessions'] = session
        context['programs'] = session.program
        return context


class SessionAddSkill(View):
    def post(self, request, *args, **kwargs):
        session = get_object_or_404(Session, pk=kwargs.get('pk'))
        data = json.loads(request.body)
        skill = ProrgamSkillGoal.objects.get(pk=data['id'])
        if skill.status == 'closed':
            skill = skill.status == 'open'
        sessionSkill, _ = SessionSkill.objects.get_or_create(session=session, skill=skill)
        try:
            sessionSkill.save()
            return JsonResponse({'add': 'add'})
        except:
            return JsonResponse({'add': False})


class SessionDeleteSkill(View):
    def delete(self, request, *args, **kwargs):
        session = get_object_or_404(Session, pk=kwargs.get('pk'))
        data = json.loads(request.body)
        skill = ProrgamSkillGoal.objects.get(pk=data['id'])
        session_skill = get_object_or_404(SessionSkill, session=session, skill=skill)
        try:
            session_skill.delete()
            return JsonResponse({'remove': 'remove'})
        except:
            return JsonResponse({'remove': False})
