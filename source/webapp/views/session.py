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


class SessionCreateView(View):
    def get(self, request, *args, **kwargs):
        program = get_object_or_404(Program, pk=kwargs.get('pk'))
        session = Session.objects.create(program=program, child=program.child, therapist=self.request.user)
        print('123')
        return redirect('webapp:session_prepear', pk=session.pk)


class SessionSkillCreateView(TemplateView):
    template_name = 'session/session_create.html'
    model = Session
    paginate_by = 5
    paginate_orphans = 0

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        session = get_object_or_404(Session, pk=self.kwargs.get('pk'))
        context['sessions'] = session
        context['programs'] = session.program
        return context
#
# class SessionAddSkill(View):
#     def post(self, request, *args, **kwargs):
#         session = get_object_or_404(Session, pk=kwargs.get('pk'))
#         data = json.loads(request.body)
#         skill_lvl = SkillLevel.objects.get(pk=data['id'])
#         session_skill, created = SessionSkill.objects.get_or_create(session=session)
#         session_skill.skill_level.add(skill_lvl)
#         print(session_skill.skill_level)
#         if created:
#             session_skill.skill_level.add(skill_lvl)
#             print(session_skill.skill_level.all())
#             return HttpResponse(session_skill)
#         return HttpResponse(session_skill)
#
#
# class SessionDeleteSkill(View):
#     def delete(self, request, *args, **kwargs):
#         session = get_object_or_404(Session, pk=kwargs.get('pk'))
#         print(session)
#         data = json.loads(request.body)
#         skill_lvl = SkillLevel.objects.get(pk=data['id'])
#         print(skill_lvl)
#         session_skill = SessionSkill.objects.get(session=session)
#         print(session_skill)
#         session_skill.skill_level.remove(skill_lvl)
#         session_skill.save()
#         return HttpResponse(session_skill)
