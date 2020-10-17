from django.contrib import messages
from django.contrib.auth.mixins import(
                                        LoginRequiredMixin,
                                        PermissionRequiredMixin
                                        )
from django.urls import reverse
from django.db import IntegrityError
from django.shortcuts import get_object_or_404
from django.views import generic
from groups.models import Group , GroupMember
from . import models

class CreateGroup(LoginRequiredMixin, generic.CreateView):
    fields = ("name", "description")
    model = models.Group

class SingleGroup(generic.DetailView):
    model = models.Group

class ListGroups(generic.ListView):
    model = models.Group


class JoinGroup(LoginRequiredMixin, generic.RedirectView):

    def get_redirect_url(self, *args, **kwargs):        #redirects to the groups detail page when joins groups
        return reverse("groups:single",kwargs={"slug": self.kwargs.get("slug")})

    def get(self, request, *args, **kwargs):                    # checks if user already a member of group
        group = get_object_or_404(Group,slug=self.kwargs.get("slug"))

        try:
            GroupMember.objects.create(user=self.request.user,group=group)

        except IntegrityError:
            messages.warning(self.request,("Warning, already a member of {}".format(group.name)))

        else:
            messages.success(self.request,"You are now a member of the {} group.".format(group.name))

        return super().get(request, *args, **kwargs)


class LeaveGroup(LoginRequiredMixin, generic.RedirectView):

    def get_redirect_url(self, *args, **kwargs):            #redirects to the groups detail page when leaves groups
        return reverse("groups:single",kwargs={"slug": self.kwargs.get("slug")})

    def get(self, request, *args, **kwargs):        # checks if user is a member of group
        try:
            membership = GroupMember.objects.filter(
                user=self.request.user,
                group__slug=self.kwargs.get("slug")
            ).get()

        except GroupMember.DoesNotExist:                # if user is not group member already
            messages.warning(
                self.request,
                "You can't leave this group because you aren't in it."
            )

        else:
            membership.delete()
            messages.success(
                self.request,
                "You have successfully left this group."
            )
        return super().get(request, *args, **kwargs)