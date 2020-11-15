from webapp.models import Test, SkillLevel


class ContextForTest:
    def all_test(self, pk, category_cod, checkbox):
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
            all_filtered_skill_code[s.skill.code] = {'previous': [], 'last': 0, 'max': count,
                                                     'empty': range(1, count+1), 'max_prev_lev': 0}

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
                            all_filtered_skill_code[key]['empty'] = range(s_l.level+1, all_filtered_skill_code[key]['max']+1)
                last = all_filtered_skill_code[key]['previous'][-1:]
                for i in last:
                    all_filtered_skill_code[key]['previous'] = range(1, i+1)
                    all_filtered_skill_code[key]['max_prev_lev'] = i

        for key, value in all_filtered_skill_code.items():
            for s in skill_level:
                if s.skill.code == key:
                    if all_filtered_skill_code[key]['max_prev_lev'] == s.level or all_filtered_skill_code[key]['max_prev_lev'] > s.level:
                        pass
                    else:
                        if all_filtered_skill_code[key]['max_prev_lev'] > 0:
                            all_filtered_skill_code[key]['last'] = range(all_filtered_skill_code[key]['max_prev_lev'] + 1, s.level + 1)
                            all_filtered_skill_code[key]['empty'] = range(s.level+1, all_filtered_skill_code[key]['max']+1)
                        else:
                            all_filtered_skill_code[key]['last'] = range(1, s.level + 1)
                            all_filtered_skill_code[key]['empty'] = range(s.level+1, all_filtered_skill_code[key]['max']+1)
        if checkbox:
            for i in all_filtered_skill_code:
                if not all_filtered_skill_code[i]['previous'] and not all_filtered_skill_code[i]['last']:
                    all_filtered_skill_code[i] = 'none'

        print(all_filtered_skill_code)
        return all_filtered_skill_code
