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
        category_code = self.request.GET.get('ABC')
        session = Session.objects.filter(program=self.object).last()
        context['child'] = self.object.child
        context['category_code'] = category_code
        context['ABC'] = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M',
                          'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
        context['session'] = session
        return context
