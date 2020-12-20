from django.contrib.auth import get_user_model
from django.core.management import call_command
from django.db.models import Model
from django.template.response import TemplateResponse
from django.test import TestCase
from django.urls import reverse

from webapp.context_for_test import ContextForTest
from webapp.models import Child, Test, SkillLevel


class LookTestResultTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        call_command('loaddata', 'fixtures/db.json', verbosity=0)


    def test_get_skill_level(self):
        c = ContextForTest()
        category_cod = 'A'
        all_sorted_skill = c.get_sorted_skill_level(category_cod=category_cod)
        self.assertIsNotNone(all_sorted_skill)
        for skill_level in all_sorted_skill:
            self.assertEqual(skill_level.skill.category.code, 'A')

    def test_get_all_filtered_skill_code(self):
        c = ContextForTest()
        get_sorted_skill_level = c.get_sorted_skill_level(category_cod='A')
        all_sorted_skill_level = c.get_all_filtered_skill_code(all_sorted_skill_level=get_sorted_skill_level)
        for i in all_sorted_skill_level:
            self.assertIn('previous', all_sorted_skill_level[i])
            self.assertIn('last', all_sorted_skill_level[i])
            self.assertIn('max', all_sorted_skill_level[i])
            self.assertIn('empty', all_sorted_skill_level[i])
            self.assertIn('max_prev_lev', all_sorted_skill_level[i])


class ResultTestCompereTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.c = ContextForTest()
        call_command('loaddata', 'fixtures/db.json', verbosity=0)
        User: Model = get_user_model()
        user, created = User.objects.get_or_create(username='admin1')
        if created:
            user.set_password('admin1')
            user.save()
        cls.skill_code = 'A3'
        cls.category_code = 'A'
        skill_level = SkillLevel.objects.filter(skill__code=cls.skill_code)
        first_skl = skill_level.first()
        second_skl = skill_level.all()[1]
        third_skl = skill_level.all()[2]
        last_skl = skill_level.last()
        print(first_skl)
        print(second_skl)
        print(third_skl)
        print(last_skl)
        child = Child.objects.create(first_name='Test_Child', age=5, first_parent='Test_Parent')
        child.therapy.add(user)
        child.save()
        previous_test = Test.objects.create(child=child, therapist=user)
        previous_test.skill_level.add(first_skl)
        previous_test.save()
        test = Test.objects.create(child=child, therapist=user, previus_test=previous_test)
        test.skill_level.add(second_skl)
        test.save()
        cls.user = user
        cls.test = test

    def setUp(self) -> None:
        self.client.login(username='admin1', password='admin1')
        url = reverse('webapp:test_result', kwargs={'pk': self.test.pk})
        self.response = self.client.get(url)

    def tearDown(self) -> None:
        self.client.logout()

    def test_create_article_success(self):
        self.assertEqual(self.response.status_code, 200)
        self.assertEqual(type(self.response), TemplateResponse)

    def test_article_create_success_data(self):
        result = self.c.all_test(self.test.pk, category_cod=self.category_code, checkbox=1)
        print(result)
        for skill in result:
            if self.skill_code != skill:
                self.assertTrue(result[skill], 'none')
            else:
                self.assertNotEqual(result[skill], 'none')

