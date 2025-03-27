from django.shortcuts import render
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from studentorg.models import Organization, OrgMember, Student, College, Program
from studentorg.forms import OrganizationForm, OrgMemberForm, StudentForm, CollegeForm, ProgramForm
from django.urls import reverse_lazy

class HomePageView(ListView):
    model = Organization
    context_object_name = 'home'
    template_name = "home.html"

class OrganizationList(ListView):
    model = Organization
    context_object_name = 'organization'
    template_name = 'org_list.html'
    paginate_by = 5

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

class ProgramCreateView(CreateView):
    model = Program
    form_class = ProgramForm
    template_name = 'prog_add.html'
    success_url = reverse_lazy('program-list')

class ProgramUpdateView(UpdateView):
    model = Program
    form_class = ProgramForm
    template_name = "prog_edit.html"
    success_url = reverse_lazy('progarm-list')

class ProgramDeleteView(DeleteView):
    model = Program
    template_name = "prog_del.html"
    success_url = reverse_lazy('program-list')