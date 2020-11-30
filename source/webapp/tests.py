from django.core.management import call_command
from django.test import TestCase

from webapp.context_for_test import ContextForTest


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
