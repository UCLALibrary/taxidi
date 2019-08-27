from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.views.generic import DetailView, ListView

from .models import (
    Unit,
    Employee,
    TravelRequest,
    Fund,
    Vacation,
    Activity,
    Approval,
    EstimatedExpense,
    ActualExpense,
)


def individual_dashboard(request):

    employee_filter = Employee.objects.filter(user=request.user)
    traveler_filter = TravelRequest.objects.filter(traveler__user=request.user)
    return render(
        request,
        "terra/individual_dashboard.html",
        {"filter1": employee_filter, "filter2": traveler_filter},
    )
