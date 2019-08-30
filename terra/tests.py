from django.test import TestCase
from django.contrib.auth.models import User
from django.core.management import call_command

from .models import (
    Unit,
    Employee,
    Fund,
    TravelRequest,
    Vacation,
    Activity,
    Approval,
    EstimatedExpense,
    ActualExpense,
)
from .templatetags.terra_extras import check_or_cross


class ModelsTestCase(TestCase):
    fixtures = ["sample_data.json"]

    def test_unit(self):
        unit = Unit.objects.get(pk=2)
        self.assertEqual(str(unit), "DIIT")
        self.assertEqual(repr(unit), "<Unit 2: DIIT>")

    def test_employee(self):
        employee = Employee.objects.get(pk=3)
        self.assertEqual(str(employee), "Joshua Gomez")
        self.assertEqual(employee.name(), "Joshua Gomez")
        self.assertEqual(repr(employee), "<Employee 3: Joshua Gomez>")

    def test_fund(self):
        fund = Fund.objects.get(pk=1)
        self.assertEqual(str(fund), "605000-LD-19900")
        self.assertEqual(repr(fund), "<Fund 1: 605000-LD-19900>")

    def test_treq(self):
        treq = TravelRequest.objects.get(pk=1)
        self.assertEqual(repr(treq), "<TReq 1: Ashton Prigge Code4lib 2020 2020>")
        self.assertEqual(str(treq), "<TReq 1: Ashton Prigge Code4lib 2020 2020>")

    def test_vacation(self):
        vac = Vacation.objects.get(pk=1)
        self.assertEqual(repr(vac), "<Vacation 1: 2020-02-17 - 2020-02-22>")
        self.assertEqual(str(vac), "<Vacation 1: 2020-02-17 - 2020-02-22>")

    def test_activity(self):
        activity = Activity.objects.get(pk=1)
        self.assertEqual(str(activity), "Code4lib 2020")
        self.assertEqual(repr(activity), "<Activity 1: Code4lib 2020>")

    def test_approval(self):
        approval = Approval.objects.get(pk=1)
        self.assertEqual(
            repr(approval), "<Approval 1: Supervisor Code4lib 2020 Ashton Prigge>"
        )
        self.assertEqual(
            str(approval), "<Approval 1: Supervisor Code4lib 2020 Ashton Prigge>"
        )

    def test_estimated_expense(self):
        estexp = EstimatedExpense.objects.get(pk=1)
        self.assertEqual(
            repr(estexp),
            "<EstimatedExpense 1: Conference Registration Code4lib 2020 Ashton Prigge>",
        )
        self.assertEqual(
            str(estexp),
            "<EstimatedExpense 1: Conference Registration Code4lib 2020 Ashton Prigge>",
        )

    def actual_expense(self):
        actexp = ActualExpense.objects.get(pk=1)
        self.assertEqual(
            repr(actexp),
            "<ActualExpense 1: Conference Registration Code4lib 2020 Ashton Prigge>",
        )
        self.assertEqual(
            str(actexp),
            "<ActualExpense 1: Conference Registration Code4lib 2020 Ashton Prigge>",
        )

    def test_unit_employee_count(self):
        sdls = Unit.objects.get(pk=3)
        self.assertEqual(sdls.employee_count(), 2)
        for x in range(5):
            u = User.objects.create_user(username=str(x))
            u.save()
            e = Employee(user=u, uid="xxxxxxxx" + str(x), unit=sdls)
            e.save()
        self.assertEqual(sdls.employee_count(), 7)

    def test_treq_international(self):
        treq = TravelRequest.objects.get(pk=1)
        self.assertEqual(treq.international(), False)
        treq.activity.country = "Germany"
        treq.activity.save()
        self.assertEqual(treq.international(), True)

    def test_treq_approved(self):
        treq = TravelRequest.objects.get(pk=1)
        self.assertEqual(treq.approved(), True)
        treq.activity.country = "Germany"
        treq.activity.save()
        self.assertEqual(treq.approved(), False)

    def test_treq_funded(self):
        treq = TravelRequest.objects.get(pk=1)
        self.assertEqual(treq.funded(), True)
        a = Approval.objects.get(pk=2)
        a.delete()
        self.assertEqual(treq.funded(), False)

    def test_expense_total_dollars(self):
        estexp = EstimatedExpense.objects.get(pk=1)
        self.assertEqual(estexp.total_dollars(), "$250.00")
        actexp = ActualExpense.objects.get(pk=1)
        self.assertEqual(actexp.total_dollars(), "$250.00")


class TemplateTagsTestCase(TestCase):
    def test_check_or_cross(self):
        self.assertEqual(
            check_or_cross(True),
            '<span class="badge badge-pill badge-success">&#10004;</span>',
        )
        self.assertEqual(
            check_or_cross(False),
            '<span class="badge badge-pill badge-danger">&times;</span>',
        )


class TestDashboardView(TestCase):

    fixtures = ["sample_data.json"]

    def test_dashboard_denies_anonymous(self):
        response = self.client.get("/dashboard", follow=True)
        self.assertRedirects(
            response, "/accounts/login/?next=/dashboard/", status_code=301
        )

    def test_call_view_loads(self):
        self.client.login(username="aprigge", password="Staples50141")
        response = self.client.get("/dashboard/")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "terra/dashboard.html")
        self.assertEqual(len(response.context["treqs"]), 1)

        
class DataLoadTestCase(TestCase):
    def test_load_units(self):
        call_command("load_units", "terra/fixtures/test_units.csv")
        unit_count = Unit.objects.all().count()
        self.assertEqual(unit_count, 2)
        arts = Unit.objects.get(name__exact="Arts Library")
        self.assertEqual(str(arts), "Arts Library")

    def test_load_employees(self):
        # Employees require Units
        call_command("load_units", "terra/fixtures/test_units.csv")
        call_command("load_employees", "terra/fixtures/test_employees.csv")
        emp_count = Employee.objects.all().count()
        self.assertEqual(emp_count, 2)
        # Edward Employee works for Sally Supervisor
        emp = Employee.objects.get(user=User.objects.get(last_name__exact="Employee"))
        sup = Employee.objects.get(user=User.objects.get(last_name__exact="Supervisor"))
        self.assertEqual(emp.supervisor, sup)

    def test_load_travel_data(self):
        # Travel data requires Employees, which require Units
        call_command("load_units", "terra/fixtures/test_units.csv")
        call_command("load_employees", "terra/fixtures/test_employees.csv")
        call_command("load_travel_data", "terra/fixtures/test_travel_data.csv")
        treq_count = TravelRequest.objects.all().count()
        self.assertEqual(treq_count, 3)
        activity_count = Activity.objects.all().count()
        # 2 people have the same activity, so count is less than treq_count
        self.assertEqual(activity_count, 2)
