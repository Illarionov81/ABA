import json

from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect
from django.views import View
from django.views.generic import DetailView

from webapp.models import Session, Program, SkillLevel, SessionSkill, Skill, ProrgamSkillGoal, ProgramSkill


class SessionDataCollectionView(DetailView):
    template_name = 'session/session_data_collection.html'
    model = Program

    def get_code_in_session(self, session):
        codes = []
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
        litera = []
        for l in ABC:
            for i in range(len(codes)):
                print(codes[i].code)
                if codes[i].code == l.code:
                    litera.append(codes[i])
        print(litera)
        return litera

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category_code = self.request.GET.get('ABC')
        session = Session.objects.filter(program=self.object).last()
        code = self.get_code_in_session(session)
        skill = Skill.objects.filter(category__code=category_code).filter()
        ABC = []
        for i in code:
            if i.category.code not in ABC:
                ABC.append(i.category.code)
        ABC.sort()
        context['code'] = code
        context['skill_code_query'] = skill.values_list('code', flat=True)
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
