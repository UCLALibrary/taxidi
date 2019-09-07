from django.views.generic.list import ListView
from django.views.generic import DetailView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

from .models import TravelRequest, Unit
from .reports import unit_report


class UserDashboard(LoginRequiredMixin, ListView):

    model = TravelRequest
    context_object_name = "treqs"
    login_url = "/accounts/login/"
    redirect_field_name = "next"

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(traveler__user=self.request.user)


class UnitDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):

    model = Unit
    context_object_name = "unit"
    login_url = "/accounts/login/"
    redirect_field_name = "next"

    def test_func(self):
        unit = self.get_object()
        return self.request.user.employee in unit.super_managers()

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["report"] = unit_report(self.object)
        return context


class UnitListView(LoginRequiredMixin, ListView):

    model = Unit
    context_object_name = "units"
    login_url = "/accounts/login/"
    redirect_field_name = "next"

    def get_queryset(self):
        return super().get_queryset().filter(type="2")
