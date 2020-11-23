from webapp.models import Test, SkillLevel


class ContextForTest:
    def all_test(self, pk, category_cod, checkbox):
        test = Test.objects.get(pk=pk)
        child_pk = test.child_id
        this_test_skill_level = test.skill_level.filter(skill__category__code=category_cod)
        all_sorted_skill_level = self.get_skill_level(category_cod)
        numbers_of_levels = self.how_mutch_skills(all_sorted_skill_level)
        all_filtered_skill_code = self.get_all_filtered_skill_code(all_sorted_skill_level, numbers_of_levels)
        self.make_old_test_data(test, all_filtered_skill_code, child_pk, category_cod)
        self.make_this_test_data(all_filtered_skill_code, this_test_skill_level)
        if checkbox:
            self.check_empty(all_filtered_skill_code)
        print(all_filtered_skill_code)
        return all_filtered_skill_code

    def how_mutch_skills(self, skill_level):
        numbers_of_levels = []
        for skl in skill_level:
            numbers_of_levels.append(skl.skill.code)
        return numbers_of_levels

    def get_skill_level(self, category_cod):
        all_sorted_skill_level = SkillLevel.objects.filter(skill__category__code=category_cod)
        return all_sorted_skill_level

    def get_all_filtered_skill_code(self, skilllevel, numbers_of_levels):
        all_filtered_skill_code = {}
        for s in skilllevel:
            count = 0
            for i in numbers_of_levels:
                if i == s.skill.code:
                    count += 1
            all_filtered_skill_code[s.skill.code] = {'previous': [], 'last': 0, 'max': count,
                                                     'empty': range(1, count+1), 'max_prev_lev': 0}
        return all_filtered_skill_code

    def check_empty(self, all_filtered_skill_code):
        for i in all_filtered_skill_code:
            if not all_filtered_skill_code[i]['previous'] and not all_filtered_skill_code[i]['last']:
                all_filtered_skill_code[i] = 'none'
        return all_filtered_skill_code

    def get_empty_range(self, i, all_filtered_skill_code, key):
        all_filtered_skill_code[key]['empty'] = range(i.level + 1, all_filtered_skill_code[key]['max'] + 1)
        return all_filtered_skill_code

    def make_old_test_data(self, test, all_filtered_skill_code, child_pk, category_cod):
        if test.previus_test:
            previous_tests = Test.objects.filter(pk__lt=test.pk, child_id=child_pk)
            for key, value in all_filtered_skill_code.items():
                for t in previous_tests:
                    for s_l in t.skill_level.filter(skill__category__code=category_cod):
                        if s_l.skill.code == key:
                            m = all_filtered_skill_code[key]
                            for i, j in m.items():
                                if i == 'previous':
                                    j.append(s_l.level)
                            self.get_empty_range(s_l, all_filtered_skill_code, key)
                all_filtered_skill_code = self.make_range_previous_test(all_filtered_skill_code, key)
        return all_filtered_skill_code

    def make_range_previous_test(self, all_filtered_skill_code, key):
        last = all_filtered_skill_code[key]['previous'][-1:]
        for i in last:
            all_filtered_skill_code[key]['previous'] = range(1, i+1)
            all_filtered_skill_code[key]['max_prev_lev'] = i
        return all_filtered_skill_code

    def make_this_test_data(self, all_filtered_skill_code, this_test_skill_level):
        for key, value in all_filtered_skill_code.items():
            for s in this_test_skill_level:
                if s.skill.code == key:
                    if all_filtered_skill_code[key]['max_prev_lev'] == s.level or all_filtered_skill_code[key]['max_prev_lev'] > s.level:
                        pass
                    else:
                        if all_filtered_skill_code[key]['max_prev_lev'] > 0:
                            all_filtered_skill_code[key]['last'] = range(all_filtered_skill_code[key]['max_prev_lev'] + 1, s.level + 1)
                            self.get_empty_range(s, all_filtered_skill_code, key)
                        else:
                            all_filtered_skill_code[key]['last'] = range(1, s.level + 1)
                            self.get_empty_range(s, all_filtered_skill_code, key)
        return all_filtered_skill_code

