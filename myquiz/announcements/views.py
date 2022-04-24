from django.views import generic
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect, render
from django.urls import reverse, reverse_lazy
from .forms import *
from django.contrib.auth.mixins import (LoginRequiredMixin)


class CreateAnnouncementView(LoginRequiredMixin, generic.CreateView):
    form_class = CreateAnnouncementForm
    template_name = 'announcements/createannouncement_form.html'

    # success_url = reverse('assignments:submit_detail')
    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.author = self.request.user

        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(CreateAnnouncementView, self).get_context_data(**kwargs)

        context['time'] = timezone.now()
        return context


class AnnouncementListView(generic.ListView):
    model = Announcement

    def get_context_data(self):

        context = super(AnnouncementListView, self).get_context_data()

        if  self.request.user.user_type ==2:
            context['object_list'] = self.request.user.announcement.all()


        #announcement = Announcement.objects.get(pk=self.kwargs['pk'])
        #context['announcement'] = announcement
        return context


class AnnouncementDetail(LoginRequiredMixin, generic.DetailView):
    model = Announcement

    def get_context_data(self, **kwargs):
        context = super(AnnouncementDetail, self).get_context_data(**kwargs)
        announcement = Announcement.objects.get(pk=self.kwargs['pk'])
        context['announcement'] = announcement
        return context

class DeleteAnnouncement(LoginRequiredMixin, generic.DeleteView):
    model = Announcement
    success_url = reverse_lazy('announcements:announcement-list')