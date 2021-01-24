import json
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from django.views import View
from django.views.generic import ListView, TemplateView, DeleteView
from webapp.models import Program, ProrgamSkillGoal, SessionSkill, HomeWork


class HomeworkListView(ListView):
    template_name = 'homework/homeworks_list.html'
    paginate_by = 15
    paginate_orphans = 0
    model = HomeWork

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        program = get_object_or_404(Program, pk=self.kwargs.get('pk'))
        homeworks = HomeWork.objects.filter(program=program)
        context['homeworks'] = homeworks
        context['program'] = program
        return context


class HomeWorkDeleteView(DeleteView):
    template_name = 'homework/homework_delete.html'
    model = HomeWork

    def get_success_url(self):
        return reverse('webapp:homeworks', kwargs={'pk': self.object.program.pk})


class HomeworkCreateView(View):
    def get(self, request, *args, **kwargs):
        program = get_object_or_404(Program, pk=kwargs.get('pk'))
        print(kwargs.get('pk'))
        homework = HomeWork.objects.create(program=program)
        return redirect('webapp:homework_update', pk=homework.pk)


class HomeworkUpdateView(TemplateView):
    template_name = 'homework/homework_create.html'
    model = HomeWork

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        homework = get_object_or_404(HomeWork, pk=self.kwargs.get('pk'))
        goal = ProrgamSkillGoal.objects.filter(skill__program=homework.program.pk)
        goal_in_homework = homework.skill.values_list('pk', flat=True)
        context['goal_in_homework'] = goal_in_homework
        context['goals'] = goal
        context['homework'] = homework
        context['programs'] = homework.program
        return context


class HomeworkAddSkill(View):
    def post(self, request, *args, **kwargs):
        homework = get_object_or_404(HomeWork, pk=kwargs.get('pk'))
        data = json.loads(request.body)
        skill = ProrgamSkillGoal.objects.get(pk=data['id'])
        homework.skill.add(skill)
        return JsonResponse({'add': 'add'})


class HomeworkDeleteSkill(View):
    def delete(self, request, *args, **kwargs):
        homework = get_object_or_404(HomeWork, pk=kwargs.get('pk'))
        data = json.loads(request.body)
        skill = ProrgamSkillGoal.objects.get(pk=data['id'])
        homework.skill.remove(skill)
        return JsonResponse({'remove': 'remove'})
