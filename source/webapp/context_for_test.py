from webapp.models import Test


class ContextForTest:
    def all_test(self, pk, category_cod):
        category_cod = category_cod
        test = Test.objects.get(pk=pk)
        this_test = {}
        previous_test = []
        tests = {}
        all_code = []
        skill_level = test.skill_level.filter(skill__category__code=category_cod)
        for s in skill_level:
            if s.skill.code not in this_test:
                this_test[s.skill.code] = []
                for key, value in this_test.items():
                    if s.skill.code == key and s.level not in value:
                        this_test[s.skill.code].append(s.level)
        if test.previus_test:
            previous_tests = Test.objects.filter(pk__lt=test.pk)
            for t in previous_tests:
                for skill_level in t.skill_level.filter(skill__category__code=category_cod):
                    if skill_level not in previous_test:
                        previous_test.append(skill_level)
            for i in previous_test:
                if i.skill.code not in tests:
                    tests[i.skill.code] = []
            for i in previous_test:
                for key, value in tests.items():
                    if i.skill.code == key and i.level not in value:
                        tests[i.skill.code].append(i.level)
        diff = {}
        for k, v in tests.items():
            all_code.append(k)
        for i, j in this_test.items():
            if i in all_code:
                pass
            else:
                diff[i] = j
        print(diff)
        print(tests)
        print(this_test)
        return tests, this_test, diff
