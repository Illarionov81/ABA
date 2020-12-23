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
        cls.first_skl = skill_level.first()
        cls.second_skl = skill_level.all()[1]
        cls.third_skl = skill_level.all()[2]
        cls.last_skl = skill_level.last()
        child = Child.objects.create(first_name='Test_Child', age=5, first_parent='Test_Parent')
        child.therapy.add(user)
        child.save()
        previous_test = Test.objects.create(child=child, therapist=user)
        previous_test.save()
        test = Test.objects.create(child=child, therapist=user, previus_test=previous_test)
        test.save()
        cls.user = user
        cls.test = test
        cls.previous_test = previous_test


    def setUp(self) -> None:
        self.client.login(username='admin1', password='admin1')
        url = reverse('webapp:test_result', kwargs={'pk': self.test.pk})
        self.response = self.client.get(url)

    def tearDown(self) -> None:
        self.client.logout()

    def test__test_result_success(self):
        self.previous_test.skill_level.add(self.first_skl)
        self.test.skill_level.add(self.second_skl)
        self.assertEqual(self.response.status_code, 200)
        self.assertEqual(type(self.response), TemplateResponse)

    def test_test_compere_success_data_1(self):
        self.previous_test.skill_level.add(self.first_skl)
        self.test.skill_level.add(self.second_skl)
        result = self.c.all_test(self.test.pk, category_cod=self.category_code, checkbox=1)
        for skill in result:
            if self.skill_code != skill:
                self.assertTrue(result[skill], 'none')
            else:
                self.assertEqual(self.skill_code, skill)
                self.assertNotEqual(result[skill], 'none')
                self.assertIn('previous', result[skill])
                self.assertIn('last', result[skill])
                self.assertIn('max', result[skill])
                self.assertIn('empty', result[skill])
                self.assertIn('max_prev_lev', result[skill])
                self.assertEqual(list(result[skill]['previous'])[0], self.first_skl.level)
                self.assertEqual(list(result[skill]['last'])[0], self.second_skl.level)
                self.assertEqual(list(result[skill]['empty'])[-1], self.last_skl.level)
                self.assertEqual(list(result[skill]['empty'])[-1], result[skill]['max'])
                self.assertTrue(list(result[skill]['last'])[0] > list(result[skill]['previous'])[0])
                self.assertEqual(list(result[skill]['previous'])[0], result[skill]['max_prev_lev'])

    def test_test_compere_success_data_2(self):
        self.previous_test.skill_level.add(self.last_skl)
        self.test.skill_level.add(self.second_skl)
        result = self.c.all_test(self.test.pk, category_cod=self.category_code, checkbox=1)
        for skill in result:
            if self.skill_code != skill:
                self.assertTrue(result[skill], 'none')
            else:
                self.assertEqual(self.skill_code, skill)
                self.assertNotEqual(result[skill], 'none')
                self.assertIn('previous', result[skill])
                self.assertIn('last', result[skill])
                self.assertIn('max', result[skill])
                self.assertIn('empty', result[skill])
                self.assertIn('max_prev_lev', result[skill])
                self.assertEqual(list(result[skill]['previous']), [1, 2, 3, 4])
                self.assertEqual(result[skill]['last'], 0)
                self.assertEqual(list(result[skill]['empty']), [])
                self.assertEqual(list(result[skill]['previous'])[-1], result[skill]['max_prev_lev'])
                self.assertEqual(result[skill]['max'], result[skill]['max_prev_lev'])

    def test_test_compere_success_data_3(self):
        self.previous_test.skill_level.add(self.last_skl)
        self.test.skill_level.add(self.second_skl)
        result = self.c.all_test(self.test.pk, category_cod=self.category_code, checkbox='')
        for skill in result:
            self.assertNotEqual(result[skill], 'none')
            self.assertIn('previous', result[skill])
            self.assertIn('last', result[skill])
            self.assertIn('max', result[skill])
            self.assertIn('empty', result[skill])
            self.assertIn('max_prev_lev', result[skill])
