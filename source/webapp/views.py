from django.shortcuts import render
from django.views.generic import DetailView
from webapp.models import Child


class ChildDetailView(DetailView):
    template_name = 'child/child_view.html'
    model = Child
