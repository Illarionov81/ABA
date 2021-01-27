import xlsxwriter
from io import BytesIO
from django.http import HttpResponse
from django.shortcuts import get_object_or_404

from webapp.models import Program, ProrgamSkillGoal, SessionSkill


def export_exel(request, **kwargs):
    skill = get_object_or_404(ProrgamSkillGoal, pk=kwargs.get('pk_skill'))
    program = get_object_or_404(Program, pk=kwargs.get('pk_program'))

    session_skill = SessionSkill.objects.filter(skill=skill, session__program=program)
    output = BytesIO()
    workbook = xlsxwriter.Workbook(output)
    worksheet = workbook.add_worksheet()

    done_with_hint = []
    done_self = []
    percent = []
    summa = []
    count = 0
    for i in session_skill:
        count += 1
        done_with_hint.append(i.done_with_hint)
        done_self.append(i.done_self)
        summa.append(i.done_self+i.done_with_hint)
        try:
            number = i.done_self/(i.done_with_hint + i.done_self)*100
        except ZeroDivisionError:
            number = 0
        percent.append(round(number,2))



    worksheet.write('A1', 'С подсказкой')
    worksheet.write('B1', 'Без подсказки')
    worksheet.write('C1', 'Проценты')
    worksheet.write('D1', 'Сумма')
    worksheet.write_column('A2', done_with_hint)
    worksheet.write_column('B2', done_self)
    worksheet.write_column('C2', percent)
    worksheet.write_column('D2', summa)

    chart = workbook.add_chart({'type': 'line'})

    chart.add_series({
        'name': 'С подсказкой',
        'values': '=Sheet1!$A$2:$A$' + str(count+1),
        'marker': {'type': 'diamond', 'size': 10},
        'data_labels': {'value': True},
    })

    chart.add_series({
        'name': 'Без подсказки',
        'values': '=Sheet1!$B$2:$B$' + str(count+1),
        'marker': {'type': 'diamond', 'size': 10},
        'data_labels': {'value': True},

    })
    chart.set_title({'name': 'С подсказкой и без подсказки'})

    chart.set_x_axis({'name': 'Сессии', 'min': 0})
    chart.set_y_axis({'name': 'Ответы', 'major_gridlines': {'visible': False}})




    chart_2 = workbook.add_chart({'type': 'line'})
    chart_2.add_series({
        'name': 'Без подсказки %',
        'values': '=Sheet1!$C$2:$C$' + str(count+1),
        'marker': {'type': 'diamond', 'size': 10},
        'data_labels': {'value': True},
    })

    chart_2.set_x_axis({'name': 'Сессии', 'min': 0})
    chart_2.set_y_axis({'name': 'Ответы без подсказки %', 'major_gridlines': {'visible': False}, 'max': 100})

    chart_3 = workbook.add_chart({'type': 'line'})
    chart_3.add_series({
        'name': 'Сумма',
        'values': '=Sheet1!$D$2:$D$' + str(count + 1),
        'marker': {'type': 'diamond', 'size': 10},
        'data_labels': {'value': True},
    })

    chart_3.add_series({
        'name': 'Без подсказки',
        'values': '=Sheet1!$B$2:$B$' + str(count + 1),
        'marker': {'type': 'diamond', 'size': 10},
        'data_labels': {'value': True},

    })
    chart_3.set_title({'name': 'С подсказкой и сумма'})

    chart.set_x_axis({'name': 'Сессии', 'min': 0})
    chart.set_y_axis({'name': 'Ответы', 'major_gridlines': {'visible': False}})

    worksheet.insert_chart('E3', chart)
    worksheet.insert_chart('M3', chart_2)
    worksheet.insert_chart('H20', chart_3)
    workbook.close()
    response = HttpResponse(content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = 'attachment;filename="some_file_name.xlsx"'
    response.write(output.getvalue())
    return response
