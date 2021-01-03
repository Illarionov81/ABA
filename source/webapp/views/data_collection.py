import json

from django.http import JsonResponse, HttpResponse, request
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from django.views import View
from django.views.generic import DetailView, CreateView

from webapp.forms import SessionAddGoal
from webapp.models import Session, Program, SkillLevel, SessionSkill, Skill, ProrgamSkillGoal, ProgramSkill


class SessionAddGoalView(CreateView):
    template_name = 'session/session_add_goal.html'
    form_class = SessionAddGoal
    model = ProrgamSkillGoal

    def form_valid(self, form):
        program = get_object_or_404(Program, pk=self.kwargs.get('pk'))
        level = get_object_or_404(SkillLevel, pk=self.kwargs.get('level'))
        goal = form.save(commit=False)
        session = Session.objects.filter(program=program).last()
        program_skill = ProgramSkill()
        program_skill.program = program
        program_skill.level = level
        session_skill = SessionSkill()
        session_skill.session_id = session.pk
        program_skill.save()
        goal.skill = program_skill
        goal.save()
        session_skill.skill_id = goal.pk
        session_skill.save()
        next_url = self.request.GET.get('next')
        return redirect(next_url)


class SessionDataCollectionView(DetailView):
    template_name = 'session/session_data_collection.html'
    model = Program

    def get_code_in_session(self, session):
        codes = []
        liters = []
        ABC = Skill.objects.all()
        for session_skill in session.skills.all():
            goal = ProrgamSkillGoal.objects.filter(session_skills=session_skill)
            for g in goal:
                add_criteria = ProgramSkill.objects.filter(goal=g)
                for add_crit in add_criteria:
                    skill_level = SkillLevel.objects.filter(program_skill=add_crit)
                    for level in skill_level:
                        skill = Skill.objects.get(levels=level)
                        if skill not in codes:
                            codes.append(skill)
        for l in ABC:
            for i in range(len(codes)):
                if codes[i].code == l.code:
                    liters.append(codes[i])
        return liters

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category_code = self.request.GET.get('ABC')
        session = Session.objects.filter(program=self.object).last()
        code = self.get_code_in_session(session)
        ABC = []
        for i in code:
            if i.category.code not in ABC:
                ABC.append(i.category.code)
        ABC.sort()
        context['code'] = code
        context['child'] = self.object.child
        context['category_code'] = category_code
        context['ABC'] = ABC
        context['session'] = session
        return context


class DoneSelf(View):
    def post(self, request, *args, **kwargs):
        data = json.loads(request.body)
        session_skill = SessionSkill.objects.get(pk=data['id'])
        session_skill.done_self += 1
        session_skill.save()
        return JsonResponse({'count': session_skill.done_self})


class DoneWithHint(View):
    def post(self, request, *args, **kwargs):
        data = json.loads(request.body)
        session_skill = SessionSkill.objects.get(pk=data['id'])
        session_skill.done_with_hint += 1
        session_skill.save()
        return JsonResponse({'count': session_skill.done_with_hint})
