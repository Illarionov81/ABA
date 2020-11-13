from webapp.models import Test, SkillLevel


class ContextForTest:
    def all_test(self, pk, category_cod):
        skilllevel = SkillLevel.objects.filter(skill__category__code=category_cod)
        category_cod = category_cod
        test = Test.objects.get(pk=pk)
        all_filtered_skill_code = {}
        numbers_of_levels = []
        for skl in skilllevel:
            numbers_of_levels.append(skl.skill.code)

        for s in skilllevel:
            count = 0
            for i in numbers_of_levels:
                if i == s.skill.code:
                    count += 1
            all_filtered_skill_code[s.skill.code] = {'previous': [], 'last': '', 'max': count, 'empty': range(count)}
        skill_level = test.skill_level.filter(skill__category__code=category_cod)

        if test.previus_test:
            previous_tests = Test.objects.filter(pk__lt=test.pk)
            for key, value in all_filtered_skill_code.items():
                for t in previous_tests:
                    for s_l in t.skill_level.filter(skill__category__code=category_cod):
                        if s_l.skill.code == key:
                            m = all_filtered_skill_code[key]
                            for i, j in m.items():
                                if i == 'previous':
                                    j.append(s_l.level)
                                    d = all_filtered_skill_code[key]['max'] - s_l.level
                                    all_filtered_skill_code[key]['empty'] = range(d)

        for key, value in all_filtered_skill_code.items():
            for s in skill_level:
                if s.skill.code == key:
                    all_filtered_skill_code[key]['last'] = s.level
                    d = all_filtered_skill_code[key]['max'] - s.level
                    all_filtered_skill_code[key]['empty'] = range(d)

        print(all_filtered_skill_code)
        return all_filtered_skill_code
