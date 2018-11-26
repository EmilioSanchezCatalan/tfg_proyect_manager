from django.http import HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test
from django.utils.decorators import method_decorator
from django.views.generic.base import RedirectView
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic.detail import DetailView
from django.urls import reverse, reverse_lazy
from core.forms import CreateTutor2Form
from login.models import Students
from login.forms import CreateStudentForm
from login.decorators import is_teacher, is_from_group, is_departaments, is_center
from .models import Tfms
from .forms import FilterPublicTfmForm, FilterTeacherTfmForm, CreateTfmForm, FilterDepartamentTfmForm, FilterCenterTfmForm

class TfmListView(ListView):
    model = Tfms
    template_name = "tfms/public_tfms_list.html"

    def get_queryset(self):
        queryset = super().get_queryset().filter(departament_validation=True, center_validation=True)
        name = self.request.GET.get("name_project", "")
        master = self.request.GET.get("formation_project", "")
        if name:
            queryset = queryset.filter(title__contains=name)
        if master:
            queryset = queryset.filter(masters_id=master)
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Tfms"
        context['form_filter'] = FilterPublicTfmForm(initial=self.request.GET.dict())
        return context

class TfmDetailView(DetailView):
    model = Tfms
    teamplate_name = "tfms/tfms_detail"

    # filtrar solo por aquellos que este validados completamente

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["students"] = Students.objects.filter(tfms_id=context['tfms'].id)
        context["back_url"] = "public_tfms_list"
        return context

@method_decorator(user_passes_test(is_teacher), name="dispatch")
class TeacherTfmListView(ListView):
    model = Tfms
    template_name = "tfms/teacher_tfms_list.html"

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(tutor1=self.request.user)
        name = self.request.GET.get("search_text", "")
        master = self.request.GET.get("formation_project", "")
        if name:
            queryset = queryset.filter(title__contains=name)
        if master:
            queryset = queryset.filter(masters_id=master)
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Tfms"
        context['is_filtering'] = self.__check_filters_is_applied(self.request.GET.dict())
        context['form_filter'] = FilterTeacherTfmForm(initial=self.request.GET.dict(), user=self.request.user)
        context['nbar'] = "tfm"
        return context

    @staticmethod
    def __check_filters_is_applied(params_dict):
        for param_name in params_dict.keys():
            if param_name != "search_text" and params_dict[param_name] != "":
                return True
        return False

@method_decorator(user_passes_test(is_teacher), name="dispatch")
class TeacherTfmDetailView(DetailView):
    model = Tfms
    teamplate_name = "tfms/tfms_detail"

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(tutor1=self.request.user)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["students"] = Students.objects.filter(tfms_id=context['tfms'].id)
        context["back_url"] = "teacher_tfms_list"
        return context

@method_decorator(user_passes_test(is_teacher), name="dispatch")
class TeacherTfmCreateView(CreateView):
    model = Tfms
    form_class = CreateTfmForm
    success_url = reverse_lazy("teacher_tfms_list")
    template_name = "tfms/tfms_create_form.html"

    def get_form_kwargs(self):
        kwargs = super(TeacherTfmCreateView, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["student_form"] = CreateStudentForm(prefix="student")
        context["tutor2_form"] = CreateTutor2Form(prefix="tutor2")
        context["back_url"] = "teacher_tfms_list"
        return context

    def post(self, request, *args, **kwargs):
        self.object = None
        form = self.get_form()
        student_form, tutor2_form = None, None
        if self.request.POST.get('has_student') == 'on':
            student_form = CreateStudentForm(
                self.request.POST,
                prefix="student",
                instance=self.__get_student_tfg(
                    self.request.POST.get('student-dni')
                )
            )
            student_val = student_form.is_valid()
        else:
            student_val = True
        if self.request.POST.get('has_tutor2') == 'on':
            tutor2_form = CreateTutor2Form(self.request.POST, prefix="tutor2")
            tutor2_val = tutor2_form.is_valid()
        else:
            tutor2_val = True
        if form.is_valid() and student_val and tutor2_val:
            return self.form_valid(form, student_form, tutor2_form)
        else:
            return self.form_invalid(form, student_form, tutor2_form)

    def form_valid(self, form, student_form=None, tutor2_form=None):
        tutor2 = self.__createtutor2(tutor2_form)
        self.__createTfm(form, tutor2)
        self.__createStudent(self.object, student_form)
        messages.success(self.request, "Creado correctamente nuevo trabajo final de master con titulo: \"" + self.object.title + "\"", 'success')
        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form, student_form=None, tutor2_form=None):
        if student_form is None:
            student_form = CreateStudentForm(prefix="student")
        if tutor2_form is None:
            tutor2_form = CreateTutor2Form(prefix="tutor2")
        
        self.__errorsForm(form)
        self.__errorsForm(student_form)
        self.__errorsForm(tutor2_form)
        return self.render_to_response(self.get_context_data(
            form=form,
            student_form=student_form,
            tutor2_form=tutor2_form
        ))
    
    def __errorsForm(self, form):
        form_errors = form.errors
        for fields_error in form_errors.keys():
            for error in form_errors[fields_error]:
                messages.error(self.request, fields_error + ": " + error, 'danger')

    def __createTfm(self, form, tutor2=None):
        self.object = form.save(commit=False)
        self.object.tutor1 = self.request.user
        self.object.tutor2 = tutor2
        self.object.save()

    @staticmethod
    def __get_student_tfg(dni):
        try:
            return Students.objects.get(dni=dni)
        except:
            return None

    @staticmethod
    def __createStudent(tfm, form=None):
        if form is not None:
            student = form.save(commit=False)
            student.tfms = tfm
            student.save()

    @staticmethod
    def __createtutor2(form=None):
        if form is not None:
            return form.save()
        else:
            return None

@method_decorator(user_passes_test(is_from_group), name="dispatch")
class TfmUpdateView(UpdateView):
    model = Tfms
    form_class = CreateTfmForm
    template_name = "tfms/tfms_update_form.html"

    def get_form_kwargs(self):
        kwargs = super(TfmUpdateView, self).get_form_kwargs()
        if self.request.user.groups.filter(name="Teachers").exists():
            kwargs['user'] = self.request.user
        else:
            kwargs['user'] = self.get_object().tutor1
        return kwargs

    def get_success_url(self):
        if self.request.user.groups.filter(name="Teachers").exists():
            return reverse('teacher_tfms_list')
        elif self.request.user.groups.filter(name="Departaments").exists():
            return reverse('departament_tfms_list')
        elif self.request.user.groups.filter(name="Centers").exists():
            return reverse('center_tfms_list')

    def get_queryset(self):
        queryset = super(TfmUpdateView, self).get_queryset()
        if self.request.user.groups.filter(name="Teachers").exists():
            queryset = queryset.filter(tutor1=self.request.user)
        elif self.request.user.groups.filter(name="Departaments").exists():
            queryset = queryset.filter(
                masters__departament=self.request.user.userinfos.departaments,
                departament_validation=None
            )
        elif self.request.user.groups.filter(name="Centers").exists():
            queryset = queryset.filter(
                masters__centers=self.request.user.userinfos.centers,
                departament_validation=True,
                center_validation=None
            )
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tfm = self.get_object()
        student = self.__get_student_tfm(tfm)
        context["student_form"] = CreateStudentForm(prefix="student", instance=student[0])
        context["number_students"] = tfm.students.all().count()
        context["tutor2_form"] = CreateTutor2Form(prefix="tutor2", instance=tfm.tutor2)
        if self.request.user.groups.filter(name="Teachers").exists():
            context["back_url"] = "teacher_tfms_list"
        elif self.request.user.groups.filter(name="Departaments").exists():
            context["back_url"] = "departament_tfms_list"
        elif self.request.user.groups.filter(name="Centers").exists():
            context["back_url"] = "center_tfms_list"
        return context
    
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        student_form, student2_form, tutor2_form = None, None, None
        form = self.get_form()
        form.instance = self.object
        if self.request.POST.get('has_student') == 'on':
            student_form = CreateStudentForm(
                self.request.POST,
                prefix="student",
                instance=self.__get_student_dni(
                    self.request.POST.get('student-dni')
                )
            )
            student_val = student_form.is_valid()
        else:
            student = self.__get_student_dni(self.request.POST.get('student-dni'))
            if student is not None:
                student.tfms = None
                student.save()
            student_val = True
        if self.request.POST.get('has_tutor2') == 'on':
            tutor2_form = CreateTutor2Form(self.request.POST, prefix="tutor2", instance=self.object.tutor2)
            tutor2_val = tutor2_form.is_valid()
        else:
            tutor2_val = True
        if form.is_valid() and student_val and tutor2_val:
            return self.form_valid(form, student_form, tutor2_form)
        else:
            return self.form_invalid(form, student_form, tutor2_form)

    def form_valid(self, form, student_form=None, tutor2_form=None):
        tutor2 = self.__createtutor2(tutor2_form)
        self.__createtfm(form, tutor2)
        self.__createStudent(self.object, student_form)
        messages.success(self.request, "Actualizado correctamente el trabajo fin de master con titulo: \"" + self.object.title + "\"", 'success')
        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form, student_form=None, tutor2_form=None):
        if student_form is None:
            student_form = CreateStudentForm(prefix="student")
        if tutor2_form is None:
            tutor2_form = CreateTutor2Form(prefix="tutor2")
        self.__errorsForm(form)
        self.__errorsForm(student_form)
        self.__errorsForm(tutor2_form)
        return self.render_to_response(self.get_context_data(
            form=form,
            student1_form=student_form,
            tutor2_form=tutor2_form
        ))
    
    def __errorsForm(self, form):
        form_errors = form.errors
        for fields_error in form_errors.keys():
            for error in form_errors[fields_error]:
                messages.error(self.request,  fields_error + ": " + error, 'danger')

    def __createtfm(self, form, tutor2=None):
        self.object = form.save(commit=False)
        self.object.tutor2 = tutor2
        self.object.save()

    @staticmethod
    def __get_student_dni(dni):
        try:
            return Students.objects.get(dni=dni)
        except:
            return None

    @staticmethod
    def __get_student_tfm(tfm):
        students = [None]
        students_list = tfm.students.all()
        if students_list.count() > 0:
            students = students_list
        return students

    @staticmethod
    def __createStudent(tfm, form=None):
        if form is not None:
            student = form.save(commit=False)
            student.tfms = tfm
            student.save()

    @staticmethod
    def __createtutor2(form=None):
        if form is not None:
            return form.save()
        else:
            return None

@method_decorator(user_passes_test(is_teacher), name="dispatch")
class TeacherTfmDelete(RedirectView):
    url = "teacher_tfms_list"
    pattern_name = 'delete_Tfm'
    
    def get_redirect_url(self, *args, **kwargs):
        Tfms.objects.filter(id=kwargs['id'], tutor1=self.request.user).delete()
        url = reverse(super().get_redirect_url(*args, **kwargs))
        return url

@method_decorator(user_passes_test(is_departaments), name="dispatch")
class DepartamentTfmListView(ListView):
    model = Tfms
    template_name = "tfms/departament_tfms_list.html"

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(masters__departament=self.request.user.userinfos.departaments, departament_validation=None)
        name = self.request.GET.get("search_text", "")
        master = self.request.GET.get("formation_project", "")
        area = self.request.GET.get("area", "")
        tutor = self.request.GET.get("tutor", "")
        if name:
            queryset = queryset.filter(title__contains=name)
        if master:
            queryset = queryset.filter(masters_id=master)
        if area:
            queryset = queryset.filter(tutor1__userinfos__areas_id=area)
        if tutor:
            queryset = queryset.filter(tutor1_id=tutor)
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Tfms"
        context['is_filtering'] = self.__check_filters_is_applied(self.request.GET.dict())
        context['form_filter'] = FilterDepartamentTfmForm(initial=self.request.GET.dict(), user=self.request.user)
        context['nbar'] = "tfm"
        return context

    @staticmethod
    def __check_filters_is_applied(params_dict):
        for param_name in params_dict.keys():
            if param_name != "search_text" and params_dict[param_name] != "":
                return True
        return False

@method_decorator(user_passes_test(is_departaments), name="dispatch")
class DepartamentTfmDetailView(DetailView):
    model = Tfms
    teamplate_name = "tfms/tfms_detail"

    def get_queryset(self):
        queryset = super().get_queryset().filter(
            masters__departament=self.request.user.userinfos.departaments,
            departament_validation=None
        )
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["students"] = Students.objects.filter(tfms_id=context['tfms'].id)
        context["back_url"] = "departament_tfms_list"
        context["can_validate"] = True
        context["validation_url"] = "departament_tfms_validation"
        return context

@method_decorator(user_passes_test(is_departaments), name="dispatch")
class DepartamentValidation(RedirectView):
    url = "departament_tfms_list"
    pattern_name = 'validation'
    
    def get_redirect_url(self, *args, **kwargs):
        tfm = Tfms.objects.get(
            id=kwargs['id'],
            masters__departament=self.request.user.userinfos.departaments,
            departament_validation=None
        )
        tfm.departament_validation = True if kwargs['validate'] == 1 else False
        tfm.save()
        url = reverse(super().get_redirect_url(*args, **kwargs))
        return url

@method_decorator(user_passes_test(is_center), name="dispatch")
class CenterTfmListView(ListView):
    model = Tfms
    template_name = "tfms/center_tfms_list.html"

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(
            masters__centers=self.request.user.userinfos.centers,
            departament_validation=True,
            center_validation=None
        )
        name = self.request.GET.get("search_text", "")
        master = self.request.GET.get("formation_project", "")
        departament = self.request.GET.get("departament", "")
        tutor = self.request.GET.get("tutor", "")
        if name:
            queryset = queryset.filter(title__contains=name)
        if master:
            queryset = queryset.filter(masters_id=master)
        if departament:
            queryset = queryset.filter(masters__departament_id=departament)
        if tutor:
            queryset = queryset.filter(tutor1_id=tutor)
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Tfms"
        context['is_filtering'] = self.__check_filters_is_applied(self.request.GET.dict())
        context['form_filter'] = FilterCenterTfmForm(initial=self.request.GET.dict(), user=self.request.user)
        context['nbar'] = "tfm"
        return context
    
    @staticmethod
    def __check_filters_is_applied(params_dict):
        for param_name in params_dict.keys():
            if param_name != "search_text" and params_dict[param_name] != "":
                return True
        return False

@method_decorator(user_passes_test(is_center), name="dispatch")
class CenterTfmDetailView(DetailView):
    model = Tfms
    teamplate_name = "tfms/tfms_detail"

    def get_queryset(self):
        queryset = super().get_queryset().filter(
            masters__centers=self.request.user.userinfos.centers,
            departament_validation=True,
            center_validation=None
        )
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["students"] = Students.objects.filter(tfms_id=context['tfms'].id)
        context["back_url"] = "center_tfms_list"
        context["can_validate"] = True
        context["validation_url"] = "center_tfms_validation"
        return context

@method_decorator(user_passes_test(is_center), name="dispatch")
class CenterValidation(RedirectView):
    url = "center_tfms_list"
    pattern_name = 'validation'
    
    def get_redirect_url(self, *args, **kwargs):
        tfm = Tfms.objects.get(
            id=kwargs['id'],
            masters__centers=self.request.user.userinfos.centers,
            departament_validation=True,
            center_validation=None
        )
        tfm.center_validation = True if kwargs['validate'] == 1 else False
        tfm.save()
        url = reverse(super().get_redirect_url(*args, **kwargs))
        return url
