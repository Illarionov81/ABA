from django.test import TestCase

from webapp.context_for_test import ContextForTest


class LookTestResultTest(TestCase):
    def setUp(self) -> None:
        pass

    def test_get_skill_level(self):
        c = ContextForTest()
        category_cod = 'A'
        all_sorted_skill = c.get_sorted_skill_level(category_cod=category_cod)
        for skill_level in all_sorted_skill:
            self.assertEqual(skill_level.skill.code, category_cod)
