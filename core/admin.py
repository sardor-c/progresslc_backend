from django.contrib import admin

from core.models import Student, Subject, Certificate, Contact


# Register your models here.

class CertificateInline(admin.TabularInline):
    model = Certificate
    extra = 0
    autocomplete_fields = ['student']
    fields = ('subject','count', 'is_active')
    show_change_link = True

class ContactInline(admin.TabularInline):
    model = Contact
    extra = 0
    autocomplete_fields = ['student']
    fields = ('student', 'phone', 'is_active')
    show_change_link = True

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'test_id',
        'first_name',
        'last_name',
        'primary_subject',
        'rating',
        'is_active',
        'created_at',
    )
    list_filter = ('primary_subject', 'is_active',)
    search_fields = ('first_name', 'last_name', 'id', 'test_id')
    ordering = ('-first_name',)
    readonly_fields = ('id', "created_at")
    list_per_page = 50

    inlines = [CertificateInline, ContactInline]

@admin.register(Certificate)
class CertificateAdmin(admin.ModelAdmin):
    list_display = ('id', 'student', 'subject', 'count', 'is_active',)
    list_filter = ('subject', 'is_active',)
    search_fields = ('id', 'student__first_name', 'student__last_name', "student__id")
    ordering = ('-id',)

    autocomplete_fields = ['student']

@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ('id','code','name_uz',)
    search_fields = ('code', 'name_uz')
    ordering = ['name_uz',]

@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('id', 'student', 'phone')
    search_fields = ('id', 'student__first_name', 'student__last_name')
    ordering = ['id']