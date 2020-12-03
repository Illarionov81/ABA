from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.views.generic import DetailView, ListView
from webapp.models import Child, Program


class IndexView(ListView):
    template_name = 'index.html'
    context_object_name = 'child'
    paginate_by = 30
    paginate_orphans = 0
    model = Child


    def get_context_data(self, *, object_list=None, **kwargs):
        if self.request.user.is_authenticated:
            context = super().get_context_data(**kwargs)
            print(context)
            user = self.request.user
            child = Child.objects.filter(therapy=user)
            context['child'] = child
            return context



class ChildDetailView(DetailView):
    template_name = 'child/child_view.html'
    model = Child

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        program = Program.objects.filter(child=self.kwargs.get('pk'))
        context['programs'] = program
        return context