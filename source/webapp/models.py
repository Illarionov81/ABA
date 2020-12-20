from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

from main import settings
from main.settings import AUTH_USER_MODEL

PROGRAM_STATUS_OPEN = 'open'
PROGRAM_STATUS_CLOSED = 'closed'
PROGRAM_STATUS_CHOICES = (
    (PROGRAM_STATUS_OPEN, 'Открыта'),
    (PROGRAM_STATUS_CLOSED, 'Закрыта')
)

SESSION_STATUS_OPEN = 'open'
SESSION_STATUS_CLOSED = 'closed'
SESSION_STATUS_CHOICES = (
    (SESSION_STATUS_OPEN, 'Открыта'),
    (SESSION_STATUS_CLOSED, 'Закрыта')
)

SKILL_STATUS_OPEN = 'open'
SKILL_STATUS_CLOSED = 'closed'
SKILL_STATUS_CHOICES = (
    (SKILL_STATUS_OPEN, 'Открыт'),
    (SKILL_STATUS_CLOSED, 'Закрыт')
)

GOAL_STATUS_OPEN = 'open'
GOAL_STATUS_CLOSED = 'closed'
GOAL_STATUS_CHOICES = (
    (GOAL_STATUS_OPEN, 'Открыт'),
    (GOAL_STATUS_CLOSED, 'Закрыт')
)


class SoftDeleteManager(models.Manager):
    def active(self):
        return self.filter(is_deleted=False)

    def deleted(self):
        return self.filter(is_deleted=True)



class Child(models.Model):
    first_name = models.CharField(max_length=100, verbose_name='Имя ребенка')
    last_name = models.CharField(max_length=100, verbose_name='Фамилия ребенка', blank=True, null=True)
    third_name = models.CharField(max_length=100, blank=True, null=True, verbose_name='Отчество ребенка')
    birthday = models.DateField(blank=True, null=True, verbose_name='Дата рождения')
    age = models.CharField(max_length=100, verbose_name='Возраст')
    address = models.TextField(max_length=1000, blank=True, null=True, verbose_name='Адрес проживания')
    characteristic = models.CharField(max_length=1000, blank=True, null=True, verbose_name='Характеристика на ребенка')
    preferences = models.CharField(max_length=1000, blank=True, null=True, verbose_name='Предпочтения ребенка')
    first_parent = models.CharField(max_length=255, verbose_name='Родитель')
    second_parent = models.CharField(max_length=255, blank=True, null=True, verbose_name='Второй родитель')
    contacts = models.CharField(max_length=200, blank=True, null=True, verbose_name='Контакты ребенка')
    created_date = models.DateTimeField(auto_now_add=True, verbose_name='Дата добавления ребенка')
    edited_date = models.DateTimeField(auto_now=True, null=True, blank=True, verbose_name='Дата редактирования')
    deleted_date = models.DateTimeField(null=True, blank=True, verbose_name='Дата удаления')
    communication_system = models.TextField(max_length=1000, blank=True, null=True, verbose_name='Система коммуникации')
    therapy = models.ManyToManyField(AUTH_USER_MODEL, through='Therapy', blank=True, related_name='therapists',
                                      verbose_name='Ребенок')
    is_deleted = models.BooleanField(default=False)

    objects = SoftDeleteManager()

    def __str__(self):
        return "%s %s" % (self.first_name, self.last_name)

    class Meta:
        verbose_name = 'Дети'
        verbose_name_plural = 'Дети'


class Therapy(models.Model):
    user = models.ForeignKey(AUTH_USER_MODEL, related_name='related_to_user', on_delete=models.CASCADE, null=True,
                             verbose_name='Терапист')
    child = models.ForeignKey(Child, blank=True, related_name='child_in_user', on_delete=models.CASCADE, null=True,
                              verbose_name='Ребенок', )

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name = 'Дети пользователя'
        verbose_name_plural = 'Дети пользователей'


class Category(models.Model):
    name = models.CharField(max_length=255, verbose_name='Название секции')
    code = models.CharField(max_length=5, verbose_name='Код секции')
    created_date = models.DateTimeField(auto_now_add=True, verbose_name='Время добавления')

    def __str__(self):
        return "%s. %s" % (self.code, self.name)

    class Meta:
        verbose_name = 'Секция'
        verbose_name_plural = 'Секции'


class Skill(models.Model):
    code = models.CharField(max_length=5,null=True, blank=True, verbose_name='Код навыка')
    name = models.CharField(max_length=255, verbose_name='Название навыка')
    category = models.ForeignKey(Category, on_delete=models.PROTECT, null=True, blank=True, related_name='skills', verbose_name='Секция')
    description = models.TextField(max_length=1000, null=True, blank=True, verbose_name='Описание навыка')
    max_level = models.PositiveSmallIntegerField(default=1, verbose_name="Количество уровней сложности")




    def __str__(self):
        return "%s. %s" % (self.code, self.name)

    class Meta:
        ordering = ('id',)
        verbose_name = 'Навык'
        verbose_name_plural = 'Навыки'


class SkillLevel(models.Model):
    skill = models.ForeignKey('Skill', on_delete=models.CASCADE, related_name='levels', verbose_name='Навык')
    level = models.IntegerField(verbose_name='Уровень')
    criteria = models.CharField(max_length=1000, null=True, blank=True, verbose_name='Критерии')



    def __str__(self):
            return "{} - {} | {}".format(self.skill.code, self.level, self.criteria)


    class Meta:
        verbose_name = 'Уровень навыка'
        verbose_name_plural = 'Уровни навыков'
        ordering = ('skill', 'level')

class ProrgamSkillGoal(models.Model):
    skill = models.ForeignKey('ProgramSkill', related_name='goal', on_delete=models.CASCADE,verbose_name='Уровень навыка')
    goal = models.CharField(max_length=1000, null=True,verbose_name='Дополнительная цель')
    status = models.CharField(max_length=20, choices=GOAL_STATUS_CHOICES, default=GOAL_STATUS_OPEN,
                              verbose_name='Статус')

    def __str__(self):
        return "{}".format(self.goal)


    class Meta:
        verbose_name = "Дополнительная цель"
        verbose_name_plural = "Дополнительные цели"


class ProgramSkill(models.Model):
    level = models.ForeignKey('SkillLevel', related_name='program_skill', on_delete=models.CASCADE, null=True,
                             verbose_name='Уровень навыка')
    program = models.ForeignKey('Program', blank=True, related_name='program_skill', on_delete=models.CASCADE, verbose_name='Программа' )
    add_creteria = models.CharField(max_length=1000, null=True, blank=True, verbose_name='Дополнительные критерии')
    status = models.CharField(max_length=20, choices=SKILL_STATUS_CHOICES, default=SKILL_STATUS_OPEN,
                              verbose_name='Статус')

    def __str__(self):
        return "%s. %s" % (self.program, self.level)

    class Meta:
        verbose_name = 'Программа ребенка'
        verbose_name_plural = 'Программы ребенка'

class Program(models.Model):
    child = models.ForeignKey('Child', on_delete=models.PROTECT, related_name='programs',
                              verbose_name='Ребенок')
    author = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='programs',
                               verbose_name='Автор')
    start_date = models.DateField(verbose_name="Дата начала")
    end_date = models.DateField(verbose_name="Дата окончания")
    skills = models.ManyToManyField('SkillLevel', through='ProgramSkill' , verbose_name='Навыки', related_name='in_programs', blank=True)
    status = models.CharField(max_length=20, choices=PROGRAM_STATUS_CHOICES, default=PROGRAM_STATUS_OPEN,
                              verbose_name='Статус')
    name = models.CharField(max_length=100, null=True, blank=True, verbose_name="Название программы")
    description = models.TextField(max_length=2000, blank=True, null=True, verbose_name="Описание программы")
    comment = models.CharField(max_length=255, null=True, blank=True, verbose_name='Комментарий к программе')
    created_date = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    edited_date = models.DateTimeField(auto_now=True, blank=True, null=True, verbose_name="Дата редактирования")
    deleted_date = models.DateTimeField(blank=True, null=True, verbose_name="Дата удаления")
    is_deleted = models.BooleanField(default=False)

    objects = SoftDeleteManager()

    def is_open(self):
        return self.status == PROGRAM_STATUS_OPEN


    def __str__(self):
        return "%s %s" % (self.child, self.created_date)

    class Meta:
        verbose_name = 'Программа'
        verbose_name_plural = 'Программы'
        ordering = ['-start_date']


class Session(models.Model):
    child = models.ForeignKey('Child', related_name='sessions', blank=True, on_delete=models.PROTECT,
                              verbose_name='Ребёнок')
    program = models.ForeignKey('Program', related_name='sessions', null=True, blank=True, on_delete=models.PROTECT,
                                verbose_name='Программа')
    therapist = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.PROTECT, blank=True, related_name='sessions')
    comment = models.TextField(max_length=1000, blank=True, null=True, verbose_name="Комментарий")
    created_date = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    edited_date = models.DateTimeField(auto_now=True, blank=True, null=True, verbose_name="Дата редактирования")
    deleted_date = models.DateTimeField(blank=True, null=True, verbose_name="Дата удаления")
    status = models.CharField(max_length=20, choices=SESSION_STATUS_CHOICES, default=SESSION_STATUS_OPEN,
                              verbose_name='Статус')

    def __str__(self):
        return "{} {} ({})".format(self.child, self.created_date.strftime('%d.%m.%Y'), self.therapist)

    class Meta:
        verbose_name = 'Сессия'
        verbose_name_plural = 'Сессии'


class SessionSkill(models.Model):
    session = models.ForeignKey('Session', related_name='skills', on_delete=models.CASCADE, verbose_name='Сессия')
    skill = models.ForeignKey('Skill', related_name='in_sessions', on_delete=models.CASCADE, verbose_name='Навык')
    stimulus = models.TextField(max_length=200, null=True, blank=True, verbose_name='Стимул')
    parent_skill = models.ForeignKey('SessionSkill', related_name='dependant_skills', on_delete=models.SET_NULL,
                                     null=True, blank=True, verbose_name='Поднавык для')
    status = models.CharField(max_length=20, choices=SKILL_STATUS_CHOICES, default=SKILL_STATUS_OPEN,
                              verbose_name="Статус")
    done_self = models.PositiveSmallIntegerField(default=0, verbose_name="Самостоятельные реакции")
    done_with_hint = models.PositiveSmallIntegerField(default=0, verbose_name="Реакции с подсказкой")

    def __str__(self):
        return "{} ({})".format(self.skill, self.stimulus)

    @property
    def total(self):
        return self.done_self + self.done_with_hint

    @property
    def success_percent(self):
        if self.total == 0:
            return 0
        return self.done_self / self.total * 100

    class Meta:
        verbose_name = 'Навыки для отработки'
        verbose_name_plural = 'Навыки для отработки'
        unique_together = ('skill', 'stimulus')


class SessionSkillExtras(models.Model):
    session_skill = models.OneToOneField('SessionSkill', on_delete=models.CASCADE, related_name='extras',
                                         verbose_name='Сессия')
    mastery_criterion = models.CharField(max_length=255, null=True, blank=True, verbose_name='Критерий мастерства')
    study_method = models.ForeignKey('StudyMethod', on_delete=models.SET_NULL, null=True, blank=True,
                                     verbose_name='Метод обучения')
    reinforcement_reaction = models.CharField(max_length=255, null=True, blank=True,
                                              verbose_name='Реакция для подкрепления')
    reinforcement_mode = models.CharField(max_length=255, null=True, blank=True, verbose_name='Режим подкрепления')
    hint_type = models.ForeignKey('HintType', on_delete=models.SET_NULL, null=True, blank=True,
                                  verbose_name='Вид подсказки')
    hint_type_delete = models.ForeignKey('HintTypeDelete', on_delete=models.SET_NULL, null=True, blank=True,
                                         verbose_name='Способ удаления подсказки')
    hint_levels = models.CharField(max_length=255, null=True, blank=True, verbose_name='Уровень подсказки')
    generalization = models.CharField(max_length=255, null=True, blank=True, verbose_name='Обобщение')
    reaction_generalization = models.CharField(max_length=255, null=True, blank=True, verbose_name='Обобщение реакции')
    stimulus_generalization = models.CharField(max_length=255, null=True, blank=True, verbose_name='Обобщение стимула')

    def __str__(self):
        return str(self.session_skill)

    class Meta:
        verbose_name = 'Детали отработки'
        verbose_name_plural = 'Детали отработки'


class Test(models.Model):
    child = models.ForeignKey('Child', on_delete=models.PROTECT, related_name='test',
                              verbose_name='Ребенок')
    therapist = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.PROTECT, null=True,
                                  related_name='therapist')
    previus_test = models.OneToOneField('Test', on_delete=models.PROTECT, null=True, blank=True,
                                        verbose_name='previus_test')
    created_date = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Время изменения')
    skill_level = models.ManyToManyField('webapp.SkillLevel', related_name='test', blank=True)

    class Meta:
        verbose_name = 'Тестирование'
        verbose_name_plural = 'Тестирование'


class StudyMethod(models.Model):
    study_method = models.CharField(max_length=255, null=True, blank=True, verbose_name='Метод обучения')

    def __str__(self):
        return "%s" % self.study_method

    class Meta:
        verbose_name = 'Метод обучения'
        verbose_name_plural = 'Методы обучения'


class HintType(models.Model):
    hint_type = models.CharField(max_length=255, null=True, blank=True, verbose_name='Вид подсказки')

    def __str__(self):
        return "%s" % self.hint_type

    class Meta:
        verbose_name = 'Вид подсказки'
        verbose_name_plural = 'Виды подсказок'


class HintTypeDelete(models.Model):
    hint_type_delete = models.CharField(max_length=255, null=True, blank=True, verbose_name='Способ удаления подсказки')

    def __str__(self):
        return "%s" % self.hint_type_delete

    class Meta:
        verbose_name = 'Метод удаления подсказки'
        verbose_name_plural = 'Методы удаления подсказки'