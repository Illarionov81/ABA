from django.contrib import admin
from webapp.models import Skill, Program, Session, Child, Category, SessionSkill, Therapy, \
    StudyMethod, HintType, HintTypeDelete, Test, SkillLevel, ProgramSkill, ProrgamSkillGoal
from django.contrib.auth.admin import UserAdmin


class ResultModelAdmin(admin.ModelAdmin):
    list_display = ['session_id', 'code_skill']
    search_fields = ['session_id', 'code_skill']
    list_filter = ['created_date', 'edited_date']
    exclude = ('deleted_date',)

    def session_id(self, obj):
        return obj.session.pk

    session_id.empty_value_display = 'Не известно'

    def code_skill(self, obj):
        return obj.skill

    code_skill.empty_value_display = 'Не известно'


class SkillLevelInline(admin.TabularInline):
    model = SkillLevel
    fields = ['level', 'criteria']


class SkillModelAdmin(admin.ModelAdmin):
    list_display = ['code', 'name']
    search_fields = ['code', 'name']
    list_filter = ['category']
    inlines = [SkillLevelInline]


class CategoryModelAdmin(admin.ModelAdmin):
    list_display = ['code', 'name']
    search_fields = ['code', 'name']


class ChildrenModelAdmin(admin.ModelAdmin):
    list_display = ["first_name", "last_name", "age", "first_parent"]
    search_fields = ["first_name"]
    list_filter = ['created_date', 'edited_date']
    exclude = ('deleted_date',)


class InlineChild(admin.StackedInline):
    model = Therapy

class InlineGoals(admin.StackedInline):
    model = ProrgamSkillGoal

class InlineSessionSkill(admin.StackedInline):
    model = SessionSkill

class InlineProgram(admin.StackedInline):
    model = ProgramSkill

class ProgramGoal (admin.ModelAdmin):
    inlines = [InlineGoals]


class UsersChildModelAdmin(admin.ModelAdmin):
    list_display = ['user', 'child']


# class TestResultModelAdmin(admin.ModelAdmin):
#     list_display = ['test', 'skill_level', 'created_date']
#     search_fields = ['test']
#     list_filter = ['created_date',  'test']
#     ordering = ['test', 'skill_level']


class TestModelAdmin(admin.ModelAdmin):
    list_display = ['pk', 'previus_test', 'child', 'therapist', 'created_date']
    search_fields = ['child']
    filter_horizontal = ('skill_level',)
    list_filter = ['created_date', 'child']


class ProgramModelAdmin(admin.ModelAdmin):
    inlines = [InlineProgram]
    list_display = ['name']
    search_fields = ['name']
    list_filter = ['created_date', 'edited_date']
    filter_horizontal = ('skills',)
    exclude = ('deleted_date',)


class UserInfoAdmin(UserAdmin):
   search_fields = ['username']


class SessionModelAdmin(admin.ModelAdmin):
    inlines = [InlineSessionSkill]
    list_display = ['id', 'program_name', 'created_date']
    search_fields = ['program_name']
    list_filter = ['created_date', 'edited_date']
    exclude = ('deleted_date',)

    def program_name(self, obj):
        return obj.program.name

    program_name.empty_value_display = 'Не известно'


admin.site.site_header = 'Administrate your website'
# admin.site.unregister(User)
# admin.site.register(User, UserInfoAdmin)
admin.site.register(Skill, SkillModelAdmin)
admin.site.register(SessionSkill)
admin.site.register(StudyMethod)
admin.site.register(HintType)
admin.site.register(HintTypeDelete)
admin.site.register(Program,ProgramModelAdmin)
admin.site.register(Therapy, UsersChildModelAdmin)
admin.site.register(Session, SessionModelAdmin)
admin.site.register(Child, ChildrenModelAdmin)
admin.site.register(Category, CategoryModelAdmin)
# admin.site.register(TestResult, TestResultModelAdmin)
admin.site.register(Test, TestModelAdmin)
admin.site.register(SkillLevel)
admin.site.register(ProgramSkill,ProgramGoal)
admin.site.register(ProrgamSkillGoal)