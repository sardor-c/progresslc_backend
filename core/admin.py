from django.contrib import admin

from core.models import *


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


class GroupMembershipInline(admin.TabularInline):
    model = GroupMembership
    extra = 0
    autocomplete_fields = ['student']
    fields = ('student', 'group','joined_at', 'is_active')
    readonly_fields = ('joined_at', 'student', 'group')
    ordering = ('student__first_name',)

class PaymentInline(admin.TabularInline):
    model = Payment
    extra = 0
    autocomplete_fields = ['student']
    readonly_fields = ('student', 'group', 'start_at', 'end_at')
    fields = ('student', 'group', 'amount','start_at', 'end_at')


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = (
        'first_name',
        'last_name',
        'test_id',
        'primary_subject',
        'rating',
        'is_active',
        'created_at',
    )
    list_filter = ('primary_subject', 'is_active',)
    search_fields = ('first_name', 'last_name', 'test_id')
    ordering = ('first_name',)
    readonly_fields = ('id', "created_at")
    list_per_page = 50

    inlines = [CertificateInline, ContactInline, GroupMembershipInline, PaymentInline]

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



@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    inlines = [GroupMembershipInline, PaymentInline]
    search_fields = ('name',)

@admin.register(GroupMembership)
class GroupMembershipAdmin(admin.ModelAdmin):
    list_display = ('group', 'student', 'joined_at', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('group__name', "student__first_name", "student__last_name")
    autocomplete_fields = ['group', 'student']

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('group', 'student', 'amount', 'start_at', 'end_at','is_debtor')
    list_filter = ('group', 'student', 'start_at', 'is_debtor')
    search_fields = ('group__name', "student__first_name", 'student__last_name',)
    autocomplete_fields = ['group', 'student']