import json

from django.shortcuts import get_object_or_404, redirect
from django.views import View
from django.views.generic import DetailView

from webapp.models import Session, Child, Program, SkillLevel, SessionSkill, Skill


class SessionDataCollectionView(DetailView):
    template_name = 'session/session_data_collection.html'
    model = Program

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category_cod = self.request.GET.get('ABC')
        session = Session.objects.filter(program=self.object).last()
        context['skills'] = Skill.objects.filter(category__code=category_cod)
        # context['child_pk'] = test.child.pk
        # context['test'] = test
        context['ABC'] = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M',
                          'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
        context['session'] = session
        return context
