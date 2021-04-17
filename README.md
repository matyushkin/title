# Зачем это нужно
Если вы пишите статью для русскоязычной IT-площадки, этот инструмент поможет подобрать лучший вариант заголовка. Если вы не знаете, интересна ли ваша тема для мира IT, ресурс поможет в этом разобраться. Если же вы не можете выбрать среди нескольких различных тем введите их поочередно в строке запроса — так вы сможете выбрать наиболее выигрышную.

Количество баллов по десятибалльной шкале соотносится с числом просмотров публикаций: чем выше балл, тем лучше ожидаемый результат. Конечно, это не отменяет того, что нужно написать интересный материал -- это лишь помощник для создания заголовка.

Если вы испытываете трудности с написанием и продвижением текстов для программистов, вы можете обратиться в редакцию [Библиотеки программиста]().

# Как это работает
Мы изучили заголовки и тексты 300 тыс. русскоязычных статей на habr.com и шести других сайтах (proglib.io, tproger.ru, dev.by, vc.ru, xakep.ru, thecode.media) и обучили на них большую нейросетевую модель. 

На самом деле ресурсом управляет не одна модель, а целых три:
1) модель-оценщик (classification): знает, сколько просмотров получали различные публикации, соотносит предложенное вами (или другой моделью) название с названиями и числом просмотров других статей и выставляет оценку
2) модель-подсказчик (feature extraction, на стадии написания): подмечает, какие сущности встречаются в статьях 
3) модель-генератор (sequence to sequence, на стадии написания): на основе введенного вами заголовка и/или короткого текста конструирует заголовки с учетом структуры других популярных заголовков, 

Все модели построены на базе модели трансформер и предобученной модели для русского языка RuBERT с последующим дообучением под каждую из задач.

# Что дальше? 
Пока что сайт анализирует только заголовки и лиды (краткие описания) статей -- то, по чему обычно выбирают, читать или нет статью. Сейчас мы работаем над инструментов анализа текста статьи и генерации кратких описаний и статей. Чтобы не создавать большую нагрузку на сервер, эти инструменты будут доступны по токену. Чтобы получить доступ, оставьте свой контакт -- мы пришлем токен, как только закончим работу над новым функционалом.