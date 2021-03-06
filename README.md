# ABA
Основные требования

Терминология

ABA - Applied Behavior Analysis - Прикладной Анализ Поведения. Область психологии, изучающая поведение живых существ и применяющая научный подход - эксперименты, сбор данных, построение графиков, анализ и т.д.
ABA-терапия - методика, основанная на ABA, и применяемая для обучения детей с расстройствами аутистического спектра навыкам самообслуживания, речи, для коррекции проблемного поведения и т.д. Может применяться для обучения любых живых существ любым навыкам.
ABBLS - справочник навыков, разделённых по категориям - навыки самобслуживания, речи, коммуникации, моторики, академические и т.д. Каждый навык в ABBLS обозначен кодом, имеет краткое и полное описание, и набор уровней и критериев достижения по каждому.
Проблемное поведение - нежелательное поведение, например, плеваться, кусаться, бить и т.д.
Терапист - сотрудник детского центра, работающий по методу ABA.
Центр - место, где проводится терапия. В частности, это проект для детского центра ABC (но он может использоваться и для других центров).


Процесс терапии
В общих чертах процесс терапии проходит так:

В центр записывается новый ребёнок.
Терапист проводит оценку навыков по всем категориям ABBLS. В тесте для каждого навыка отмечается, на каком уровне находится ребёнок - от 0 до максимального в ABBLS.
Составляется программа - список навыков для отработки на долгосрочный период - обычно больше 1 месяца.
Регулярно проводятся сессии - занятия с ребёнком. На каждой сессии отрабатывается какая-то часть навыков из программы и ведётся сбор данных об успешной и неуспешной работе.
По собранным данным строятся графики, чтобы оценить, насколько навык успешно освоен.
По освоенным навыкам родителям даётся домашнее задание для отработки дома.


Справочник
Справочник называется ABBLS и представляет собой список базовых навыков, разделённых по категориям: коммуникативные, самообслуживания, игры, мелкая моторика, крупная моторика и т.д.

Категории обозначены буквами от A до Z и имеют название.
Навыки обозначены буквой категории + номер, например A1, B2, C3, и т.д.
Тераписты ориентируются по кодам, поэтому их нужно обязательно везде выводить.
У навыков есть название, описание и может быть несколько уровней.
У каждого уровня есть критерии.
В простейшем случае у навыка может быть 1 уровень - навык либо есть, либо нет.
Категории, навыки и уровни уже вбиты в базу, дамп прилагается.

Кроме ABBLS в справочнике может быть Manuals - руководство по обучению конкретным навыкам, ТЗ по этой части будет написано позже, пока не рассматривайте её.

Оценка навыков
Оценка навыков или предварительное тестирование - процесс оценки навыков ребёнка, какие навыки у него уже есть. Проводится при поступлении нового ребёнка в центр и время от времени повторяется.

Тестирование проводится по всем навыкам ABBLS
Для каждого навыка отмечается его уровень (если не отмечено, значит 0).
Тестирование проводится в игровой форме и может быть без определённого порядка, поэтому должна быть возможность легко и быстро переключиться на любой навык - в 1-2 клика + небольшая прокрутка.
Результаты каждого предыдущего теста наслаиваются поверх предыдущих (как коммиты в гите). При выводе или экспорте нужно выводить их все.
Для каждого тестирования нужно хранить дату и пользователя, кто его проводил.
Вывести легенду - терапист - время - цвета тестов.
При выводе нужно обозначить результаты предыдущих тестов и выбранного,  разными цветами.
Нужна печатная версия.
Вывод формы и результатов теста желательно сделать похожим на столбики в бумажном документе (он прилагается).


Программа
Программа составляется по итогу оценки, и в неё входят навыки из ABBLS.Может быть выбран один или несколько уровней.

В программу могут быть включены навыки, которых нет в ABBLS. Для них нужно указать название и критерии.
В программу могут быть включены критерии, которых нет в ABBLS для любого навыка.
К уровню навыка могут быть прописаны дополнительные цели. Например, навык "Назвать части тела" может иметь цели "Рука", "Нога", "Голова" и т.д.
У одного навыка может быть несколько дополнительных целей и они выводятся отдельно от критериев
Если хоть одна цель или критерий открыты, то программа считается открытой
Должны быть статусы (открыто, закрыто) у критериев и у дополнительной цели
В программе сохраняется дата, когда она была составлена и обозначается период, до какой даты она будет активна.
В программе сохраняется, кто её составил или менял.
Нужна печатная редактируемая версия.


Сессия
Сессия - это занятие проводимое с ребёнком. Обычно она длится 2 часа и на ней отрабатываются навыки из программы, а также ведётся сбор данных.

Уровни навыков для сессии берутся из активной программы ребёнка, по умолчанию добавляются из открытых уровней навыков предыдущей сессии
Если Уровень навыка имеет несколько целей, каждая цель включается отдельно. Таким образом навык может повторяться в сессии несколько раз с разными целями.
Должна быть возможность добавить навыки НЕ из программы и даже не из ABBLS (по аналогии с программой), при этом они включаются в программу.(оставить эту задачу на потом)
Реализовать ограничение по времени проведения сессии до 2 часов (оставить эту задачу на потом)
Для каждой сессии отмечается дата и терапист, который вёл.
Один и тот же набор навыков может отрабатываться с разными терапистами в течение нескольких сессий. По умолчанию нужно брать навыки из предыдущей сессии, дальше терапист их может поменять.

Примечание

Не можем менять данные в детальном просмотре сессии которая уже была


Cбор данных
В течение сессии ведётся сбор данных - ведётся счёт самостоятельных и ответов с подсказкой.

Счётчики ведутся индивидуально для каждого навыка на каждой сессии.
Счётчики нельзя менять просто так, только кликать по +1 во время сессии.
В интерфейсе должна быть возможность быстро переключаться между разными навыками из сессии.
Счётчики не должны тормозить, т.к. ответы могут даваться очень быстро.
Счётчики должны давать заметный визуальный отклик, когда ставится +1.
Должна быть возможность БЫСТРО добавить навык в сессию даже на этом этапе.
Реализовать защитой от спама в js. Нужно заблокируйте кнопку после отправки запроса и разблокируйте после получения ответа.
Подумать над защитой от спама. Например, сделать так, чтобы запрос отправлялся не сразу, а если на счётчик кликнули несколько раз, то только через небольшой период после последнего клика.

Примечание

Кнопки должны быть большими чтоб по ним не промахивались,+- не обозначать у них так не принято, должны быть выделены цветом, прям на кнопке вывести сколько раз нажато


Анализ
Если процент самостоятельных ответов в течение 2 сессий подряд >= 80, навык в программе становится закрытым

Закрытый навык считается отработанным. Его нельзя добавить в сессию или скопировать из предыдущей сессии, сбор данных по нему не ведётся.
Навык в программе может быть закрыт вручную по решению тераписта.
Навык в программе может быть открыт по решению тераписта.
Навык может быть поставлен на паузу - даже если он ещё не отработан. В этом случае он ведёт себя как закрытый и не появляется в сессиях, пока паузу не отменят.

По результатам нескольких сессий строятся графики:

Количество самостоятельных и ответов с подсказкой по сессиям.
Количество самостоятельных и общее количество ответов по сессиям.
Процент самостоятельных ответов от общего количества по сессиям.
На оси X нужно вывести номера сессий (просто порядковые номера от 1 до N) и даты, когда сессия проводилась (даты могут повторяться, т.к. в один день может быть несколько сессий).
Нужен экспорт графиков в эксель.
По возможности нужно сделать вывод вертикальной черты на графиках когда отработка навыка возобновляется после паузы.
Экспорт графиков с подписями по каждой сессии в эксель. Графики строятся с выбранной сессии до первой по данной программе, по каждому навыку (уровню + цели) в сессии.



Домашнее задание
Терапист может составить домашнее задание по программе для родителей.

В ДЗ входят навыки из программы, чаще всего - отработанные.
Нужна печатная редактируемая версия.
Вывод - всё то же самое, что в программе + поле для целей (где они есть) / комментариев для родителей.


Требования к вёрстке

Нужна хорошая адаптивная мобильная вёрстка, чтобы приложением было удобно пользоваться на мобильных устройствах.


Роли в системе
С доступом в админку:

Клинический директор - суперадмин.
Ассистент клинического директора - не может менять роли пользователей.

Без доступа в админку:

Терапист - ведёт терапию, сбор данных и т.д.
Кейс - терапист + может менять программы закреплённых за ним детей и составлять ДЗ для родителей.
Родитель - видит программу, видит ДЗ.
