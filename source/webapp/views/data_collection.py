import json

from django.shortcuts import get_object_or_404, redirect
from django.views import View
from django.views.generic import DetailView

from webapp.models import Session, Child, Program, SkillLevel, SessionSkill, Skill, ProrgamSkillGoal, ProgramSkill


class SessionDataCollectionView(DetailView):
    template_name = 'session/session_data_collection.html'
    model = Program

    def get_code(self, session):
        codes = []
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
        return codes

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category_code = self.request.GET.get('ABC')
        session = Session.objects.filter(program=self.object).last()
        code = self.get_code(session)
        print(code)
        skill = Skill.objects.filter(category__code=category_code).filter()
        context['code'] = code
        context['skill_code_query'] = skill.values_list('code', flat=True)
        context['child'] = self.object.child
        context['category_code'] = category_code
        context['ABC'] = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M',
                          'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
        context['session'] = session
        return context

    def post(self, request, *args, **kwargs):
        test = get_object_or_404(Test, pk=self.kwargs.get('pk'))
        data = json.loads(request.body)
        skill_lvl = SkillLevel.objects.get(pk=data['id'])
        code = skill_lvl.skill.code

        for i in test.skill_level.all():
            if skill_lvl == i:
                test.skill_level.remove(i)
                test.save()
                return redirect('webapp:child_update_test', pk=test.pk)
            if code == i.skill.code:
                test.skill_level.remove(i)
        test.skill_level.add(skill_lvl)
        test.save()
        return redirect('webapp:child_update_test', pk=test.pk)