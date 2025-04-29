from django.shortcuts import render
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from studentorg.models import Organization, OrgMember, Student, College, Program
from studentorg.forms import OrganizationForm, OrgMemberForm, StudentForm, CollegeForm, ProgramForm
from django.urls import reverse_lazy
from typing import Any
from django.db.models.query import QuerySet
from django.db.models import Q
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.db.models import Count
from django.db import connection


@method_decorator(login_required, name="dispatch")

class HomePageView(ListView):
    model = Organization
    context_object_name = 'home'
    template_name = "home.html"

class OrganizationList(ListView):
    model = Organization
    context_object_name = 'organization'
    template_name = 'org_list.html'
    paginate_by = 5

    def get_queryset(self, *args, **kwargs):
        qs = super(OrganizationList, self).get_queryset(*args, **kwargs)
        if self.request.GET.get("q") !=None:
            query = self.request.GET.get('q')
            qs = qs.filter(Q(name__icontains=query) |
                           Q(college__college_name__icontains=query) |
                           Q(description__icontains=query))
        return qs
 
class OrganizationCreateView(CreateView):
    model = Organization
    form_class = OrganizationForm
    template_name = 'org_add.html'
    success_url = reverse_lazy('organization-list')

class OrganizationUpdateView(UpdateView):
    model = Organization
    form_class = OrganizationForm
    template_name = "org_edit.html"
    success_url = reverse_lazy('organization-list')

class OrganizationDeleteView(DeleteView):
    model = Organization
    template_name = "org_del.html"
    success_url = reverse_lazy('organization-list')

class OrgMemberList(ListView):
    model = OrgMember
    context_object_name = 'orgmember'
    template_name = 'orgmem_list.html'
    paginate_by = 5

    def get_queryset(self, *args, **kwargs):
        qs = super(OrgMemberList, self).get_queryset(*args, **kwargs)
        if self.request.GET.get("q") !=None:
            query = self.request.GET.get('q')
            qs = qs.filter(Q(student__firstname__icontains=query) |
                           Q(student__lastname__icontains=query) |
                           Q(date_joined__icontains=query))
        return qs

class OrgMemberCreateView(CreateView):
    model = OrgMember
    form_class = OrgMemberForm
    template_name = 'orgmem_add.html'
    success_url = reverse_lazy('orgmember-list')

class OrgMemberUpdateView(UpdateView):
    model = OrgMember
    form_class = OrgMemberForm
    template_name = "orgmem_edit.html"
    success_url = reverse_lazy('orgmember-list')

class OrgMemberDeleteView(DeleteView):
    model = OrgMember
    template_name = "orgmem_del.html"
    success_url = reverse_lazy('orgmember-list')

class StudentList(ListView):
    model = Student
    context_object_name = 'student'
    template_name = 'student_list.html'
    paginate_by = 5

    def get_queryset(self, *args, **kwargs):
        qs = super(StudentList, self).get_queryset(*args, **kwargs)
        if self.request.GET.get("q") !=None:
            query = self.request.GET.get('q')
            qs = qs.filter(Q(student_id__icontains=query) |
                           Q(firstname__icontains=query) |
                           Q(lastname__icontains=query) |
                           Q(middlename__icontains=query))
        return qs

class StudentCreateView(CreateView):
    model = Student
    form_class = StudentForm
    template_name = 'student_add.html'
    success_url = reverse_lazy('students-list')

class StudentUpdateView(UpdateView):
    model = Student
    form_class = StudentForm
    template_name = "student_edit.html"
    success_url = reverse_lazy('students-list')

class StudentDeleteView(DeleteView):
    model = Student
    template_name = "student_del.html"
    success_url = reverse_lazy('students-list')

class CollegeList(ListView):
    model = College
    context_object_name = 'college'
    template_name = 'college_list.html'
    paginate_by = 5

    def get_queryset(self, *args, **kwargs):
        qs = super(CollegeList, self).get_queryset(*args, **kwargs)
        if self.request.GET.get("q") !=None:
            query = self.request.GET.get('q')
            qs = qs.filter(Q(college_name__icontains=query))
        return qs

class CollegeCreateView(CreateView):
    model = College
    form_class = CollegeForm
    template_name = 'college_add.html'
    success_url = reverse_lazy('colleges-list')

class CollegeUpdateView(UpdateView):
    model = College
    form_class = CollegeForm
    template_name = "college_edit.html"
    success_url = reverse_lazy('colleges-list')

class CollegeDeleteView(DeleteView):
    model = College
    template_name = "college_del.html"
    success_url = reverse_lazy('colleges-list')

class ProgramList(ListView):
    model = Program
    context_object_name = 'prog'
    template_name = 'prog_list.html'
    paginate_by = 5

    def get_queryset(self, *args, **kwargs):
        qs = super(ProgramList, self).get_queryset(*args, **kwargs)
        if self.request.GET.get("q") !=None:
            query = self.request.GET.get('q')
            qs = qs.filter(Q(prog_name__icontains=query) |
                           Q(college__college_name__icontains=query))
        return qs

class ProgramCreateView(CreateView):
    model = Program
    form_class = ProgramForm
    template_name = 'prog_add.html'
    success_url = reverse_lazy('program-list')

class ProgramUpdateView(UpdateView):
    model = Program
    form_class = ProgramForm
    template_name = "prog_edit.html"
    success_url = reverse_lazy('program-list')

class ProgramDeleteView(DeleteView):
    model = Program
    template_name = "prog_del.html"
    success_url = reverse_lazy('program-list')

def timeline_chart_data(request):
    data = (
        OrgMember.objects.values('date_joined')
        .annotate(member_count=Count('id'))
        .order_by('date_joined')
    )
    labels = [entry['date_joined'].strftime('%Y-%m-%d') for entry in data]
    counts = [entry['member_count'] for entry in data]

    response_data = {
        "labels": labels,  
        "datasets": [
            {
                "label": "New Members",
                "data": counts,  
                "backgroundColor": "rgba(54, 162, 235, 0.5)",  
                "borderColor": "rgba(54, 162, 235, 1)",
                "borderWidth": 1,
            }
        ],
    }

    return JsonResponse(response_data)

def scatter_plot_data(request):

    data = (
        College.objects.annotate(
            org_count=Count('organization'),  
            member_count=Count('organization__orgmember')  
        )
        .values('college_name', 'org_count', 'member_count')
    )

    
    chart_data = []
    for entry in data:
        chart_data.append({
            "x": entry['org_count'], 
            "y": entry['member_count'],  
            "college": entry['college_name']  
        })

    response_data = {
        "datasets": [
            {
                "label": "Colleges",
                "data": chart_data,
                "backgroundColor": "rgba(75, 192, 192, 0.5)",
                "borderColor": "rgba(75, 192, 192, 1)",
                "borderWidth": 1,
            }
        ],
    }

    return JsonResponse(response_data)

def popular_organization_by_college(request):
    data = (
        OrgMember.objects
        .values('organization__college__college_name', 'organization__name')
        .annotate(member_count=Count('id'))
        .order_by('organization__college__college_name', '-member_count')
    )


    college_data = {}
    for entry in data:
        college_name = entry['organization__college__college_name']
        organization_name = entry['organization__name']
        member_count = entry['member_count']

        if college_name not in college_data:
            college_data[college_name] = {
                "organization": organization_name,
                "members": member_count
            }


    labels = list(college_data.keys())  
    counts = [info['members'] for info in college_data.values()]  
    organizations = [info['organization'] for info in college_data.values()]  

    response_data = {
        "labels": labels,
        "datasets": [
            {
                "label": "Most Popular Organization",
                "data": counts,  
                "backgroundColor": "rgba(75, 192, 192, 0.5)",
                "borderColor": "rgba(75, 192, 192, 1)",
                "borderWidth": 1,
            }
        ],
        "organization_names": organizations, 
    }

    return JsonResponse(response_data)

def membership_distribution_by_organization(request):
    
    data = (
        OrgMember.objects
        .values('organization__name')  
        .annotate(member_count=Count('id'))  
        .order_by('-member_count')  
    )

    labels = [entry['organization__name'] for entry in data]  
    counts = [entry['member_count'] for entry in data]  

    response_data = {
        "labels": labels, 
        "datasets": [
            {
                "label": "Membership Distribution",
                "data": counts,  
                "backgroundColor": [
                    "rgba(255, 99, 132, 0.5)",
                    "rgba(54, 162, 235, 0.5)",
                    "rgba(255, 206, 86, 0.5)",
                    "rgba(75, 192, 192, 0.5)",
                    "rgba(153, 102, 255, 0.5)",
                    "rgba(255, 159, 64, 0.5)",
                ],  
                "borderColor": [
                    "rgba(255, 99, 132, 1)",
                    "rgba(54, 162, 235, 1)",
                    "rgba(255, 206, 86, 1)",
                    "rgba(75, 192, 192, 1)",
                    "rgba(153, 102, 255, 1)",
                    "rgba(255, 159, 64, 1)",
                ],
                "borderWidth": 1,
            }
        ],
    }

    return JsonResponse(response_data)


def bubble_chart_data(request):
    
    data = (
        College.objects.annotate(
            org_count=Count('organization'), 
            member_count=Count('organization__orgmember'),  
            student_count=Count('program__student')  
        )
        .values('college_name', 'org_count', 'member_count', 'student_count')
    )

    
    chart_data = []
    for entry in data:
        chart_data.append({
            "x": entry['member_count'],  
            "y": entry['org_count'],  
            "r": entry['student_count'] / 10 
        })

    labels = [entry['college_name'] for entry in data]  

    response_data = {
        "datasets": [
            {
                "label": "Colleges",
                "data": chart_data,
                "backgroundColor": "rgba(54, 162, 235, 0.5)",
                "borderColor": "rgba(54, 162, 235, 1)",
                "borderWidth": 1,
            }
        ],
        "labels": labels,  
    }

    return JsonResponse(response_data)