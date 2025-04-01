from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView, DeleteView
)
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.shortcuts import redirect

from .models import Advert, Respond
from .forms import AdvertForm, RespondForm
from .filters import RespondFilter


class IndexView(ListView):
    template_name = 'index.html'
    model = Advert
    context_object_name = 'adverts'
    ordering = '-time'
    paginate_by = 10


class AdvertDetail(DetailView):
    template_name = 'advert.html'
    model = Advert
    context_object_name = 'advert'


class AdvertCreate(LoginRequiredMixin, CreateView):
    template_name = 'advert_edit.html'
    model = Advert
    form_class = AdvertForm

    def post(self, request, *args, **kwargs):
        advert = Advert(
            author=request.user,
            category=request.POST['category'],
            header=request.POST['header'],
            content=request.POST['content']
        )
        advert.save()
        return redirect(f'/adverts/{advert.id}/')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Создание объявления'
        return context


class AdvertUpdate(LoginRequiredMixin, UpdateView):
    template_name = 'advert_edit.html'
    model = Advert
    form_class = AdvertForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Редактирование объявления'
        return context


# class AdvertDelete(LoginRequiredMixin, DeleteView):
#     template_name = 'advert_delete.html'
#     model = Advert
#     success_url = reverse_lazy('index')


class RespondList(LoginRequiredMixin, ListView):
    template_name = 'responds.html'
    model = Respond
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = RespondFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        try:
            responds = self.filterset.qs.filter(advert__author=self.request.user).select_related('advert')
            adverts = set()
            for respond in responds:
                 adverts.add(respond.advert)
            context['adverts'] = adverts
            context['responds'] = responds
        except Respond.DoesNotExist:
            context['responds'] = None
        return context


class RespondDetail(LoginRequiredMixin, DetailView):
    template_name = 'respond.html'
    model = Respond
    context_object_name = 'respond'


class RespondCreate(LoginRequiredMixin, CreateView):
    template_name = 'respond_create.html'
    model = Respond
    form_class = RespondForm

    def post(self, request, *args, **kwargs):
        respond = Respond(
            advert=Advert.objects.get(id=request.GET['advert_id']),
            author=request.user,
            content=request.POST['content']
        )
        respond.save()
        return redirect('/')


@login_required
def accept_respond(request, **kwargs):
    respond = Respond.objects.get(id=kwargs['pk'])
    respond.accepted = True
    respond.save(update_fields=['accepted'])
    return redirect('/responds/')


@login_required
def delete_respond(request, **kwargs):
    Respond.objects.filter(id=kwargs['pk']).delete()
    return redirect('/responds/')
