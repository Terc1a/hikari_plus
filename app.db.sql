BEGIN TRANSACTION;
CREATE TABLE IF NOT EXISTS news (
	id INTEGER NOT NULL, 
	title VARCHAR(100), 
	descr VARCHAR(1000), 
	version VARCHAR(10), 
	create_date VARCHAR(25), 
	to_send BOOLEAN, 
	PRIMARY KEY (id)
);
CREATE TABLE IF NOT EXISTS tag (
	id INTEGER NOT NULL, 
	title VARCHAR(100), 
	descr VARCHAR(1000), 
	PRIMARY KEY (id)
);
CREATE TABLE IF NOT EXISTS to_do (
	id INTEGER NOT NULL, 
	title VARCHAR(100), 
	tag VARCHAR(50), 
	descr VARCHAR(1000), 
	create_date VARCHAR(25), 
	close_date VARCHAR(25), 
	is_complete BOOLEAN, 
	PRIMARY KEY (id)
);
INSERT INTO "news" ("id","title","descr","version","create_date","to_send") VALUES (1,'Добавлен раздел "Что нового"','<p>На этой странице будет публиковаться информация об обновлениях и различных нововведениях, связанных с этим проектом, а так же уведомления о различных скидках и акциях</p>
','0.22','2025-01-09 04:36:32',0);
INSERT INTO "news" ("id","title","descr","version","create_date","to_send") VALUES (2,'Тестовая','<p>Введите описание новости</p>
','0.22','2025-01-09 04:37:27',0);
INSERT INTO "tag" ("id","title","descr") VALUES (2,'Health','Проект по здоровью.<br>В него входят задачи, связанные с моим здоровьем');
INSERT INTO "tag" ("id","title","descr") VALUES (3,'Life','Проект по моей жизни.<br>
В него входят задачи, связанные с моей бытовой жизнью');
INSERT INTO "tag" ("id","title","descr") VALUES (4,'TodoApp','Проект менеджера задач.<br>
Включает в себя задачи по данному проекту');
INSERT INTO "tag" ("id","title","descr") VALUES (5,'TodoApp_admin','Проект админки менеджера задач.<br>
Cодержит в себе задачи по админке менеджера');
INSERT INTO "tag" ("id","title","descr") VALUES (6,'TodoApp_list','Задачи по основной странице менеджера задач.<br>
Cодержит в себе задачи по странице со списком задач');
INSERT INTO "tag" ("id","title","descr") VALUES (7,'Finance','Содержит в себе задачи по финансовым вопросам');
INSERT INTO "tag" ("id","title","descr") VALUES (8,'TodoApp_stats','Проект содержит в себе задачи по тегам');
INSERT INTO "to_do" ("id","title","tag","descr","create_date","close_date","is_complete") VALUES (2,'Создать возможность указывать тему помимо названия задачи','TodoApp','В будущем хочу чтобы все задачи были разделены по отдельным страницам в зависимости от тематики','2024-12-20 00:00:00','2025-01-03 19:34:00',1);
INSERT INTO "to_do" ("id","title","tag","descr","create_date","close_date","is_complete") VALUES (3,'Добавить анимированные снежинки на фон сайта','TodoApp','','2024-12-20 00:00:00','2025-01-03 19:34:00',1);
INSERT INTO "to_do" ("id","title","tag","descr","create_date","close_date","is_complete") VALUES (5,'Выводить список задач рекурсивно','TodoApp','Задачи должны выводиться в обратном порядке(сорт по айди от большего к меньшему)','2024-12-20 00:00:00','2025-01-03 19:34:00',1);
INSERT INTO "to_do" ("id","title","tag","descr","create_date","close_date","is_complete") VALUES (6,'Создать отдельный блок для навигации по приложению','TodoApp','Блок должен располагаться слева в виде списка','2024-12-20 00:00:00','2025-01-03 19:34:00',1);
INSERT INTO "to_do" ("id","title","tag","descr","create_date","close_date","is_complete") VALUES (7,'Добавить всплывающее окно','TodoApp','При нажатии на кнопку, должно открываться окно создания новой задачи поверх всех остальных','2024-12-20 00:00:00','2025-01-03 19:34:00',1);
INSERT INTO "to_do" ("id","title","tag","descr","create_date","close_date","is_complete") VALUES (8,'Сохранять датувремя создания задачи и ее изменения','TodoApp','Использовать datetime<br>
Потом можно <strong>визуализировать</strong> свою активность через графики','2024-12-22 23:42:51','2024-12-22 23:42:55',1);
INSERT INTO "to_do" ("id","title","tag","descr","create_date","close_date","is_complete") VALUES (9,'Создать страницу статистики','TodoApp','Разместить там нав-меню и графики','2024-12-25 21:44:43','2024-12-25 21:44:47',1);
INSERT INTO "to_do" ("id","title","tag","descr","create_date","close_date","is_complete") VALUES (10,'Починить редактирование записей','TodoApp','','2024-12-25 21:45:18','2024-12-25 21:45:24',1);
INSERT INTO "to_do" ("id","title","tag","descr","create_date","close_date","is_complete") VALUES (11,'Скрывать описание задачи, если оно превышает одну строку','TodoApp','Через visibility не работает<br>
Возможно имеет смысл на главной странице показывать только превью, без кнопок,<br>
затем при клике на запись открывать ее в новой странице, где описание не ограничено ничемм','2025-01-03 13:32:27','2025-01-03 14:11:37',1);
INSERT INTO "to_do" ("id","title","tag","descr","create_date","close_date","is_complete") VALUES (12,'Добавить в зарядку 5 отжиманий','Health','Это должно быть не сильно дискомфортно, можно попробовать отжиматься на улице в перчатках','2024-12-25 21:47:06','2024-12-29 16:48:55',1);
INSERT INTO "to_do" ("id","title","tag","descr","create_date","close_date","is_complete") VALUES (13,'Чистить зубы каждый вечер','Health','','2024-12-25 21:48:08','2024-12-27 15:34:47',1);
INSERT INTO "to_do" ("id","title","tag","descr","create_date","close_date","is_complete") VALUES (14,'Сделать смежный график на странице статистики','TodoApp','Пока нет данных для того, чтобы сделать его','2024-12-29 23:41:09','2024-12-29 23:41:21',1);
INSERT INTO "to_do" ("id","title","tag","descr","create_date","close_date","is_complete") VALUES (15,'Выбирать теги из выпадающего списка','TodoApp_list','<s>Новые теги добавлять на странице админки</s><br>
При создании задачи по проекту выбирать тег из выпадающего списка','2025-01-01 04:01:00','2025-01-01 04:09:49',1);
INSERT INTO "to_do" ("id","title","tag","descr","create_date","close_date","is_complete") VALUES (16,'Создать страницу админки','TodoApp_admin','Там можно будет создавать теги(проекты)<br>
Выбирать тему сайта<br>
Что-то еще...','2024-12-27 15:36:32','2024-12-30 01:26:45',1);
INSERT INTO "to_do" ("id","title","tag","descr","create_date","close_date","is_complete") VALUES (17,'Текст описания задачи должен быть белого цвета','TodoApp_list','','2024-12-27 18:54:13','2024-12-27 23:40:22',1);
INSERT INTO "to_do" ("id","title","tag","descr","create_date","close_date","is_complete") VALUES (18,'Сверстать страницу админки','TodoApp_admin','<p>Содержимое:<br />
<s>1. Форма добавления тегов(через модальное окно)</s><br />
<s>2. Форма выбора темы сайта - не знаю как изменять тему на всех страницах сразу<br />
3. Форма активации/деактивации снежинок</s></p>
','2025-01-05 03:40:05','2025-01-05 03:40:09',1);
INSERT INTO "to_do" ("id","title","tag","descr","create_date","close_date","is_complete") VALUES (19,'Сделать единое nav-menu для всех страниц сайта','TodoApp','','2024-12-30 01:27:16','2025-01-02 03:08:46',1);
INSERT INTO "to_do" ("id","title","tag","descr","create_date","close_date","is_complete") VALUES (20,'Выбирать список тегов из Tag','TodoApp_list','Cейчас выборка идет из тегов, которые присвоены задачам(относится и к списку тегов в nav-menu)','2025-01-01 04:10:37','2025-01-02 02:44:28',1);
INSERT INTO "to_do" ("id","title","tag","descr","create_date","close_date","is_complete") VALUES (21,'Добавить кнопку "Скрыть выполненные"','TodoApp_list','При нажатии на кнопку все задачи со статусом is_complete=1 пропадают со страницы','2025-01-01 04:15:41','2025-01-03 10:21:36',1);
INSERT INTO "to_do" ("id","title","tag","descr","create_date","close_date","is_complete") VALUES (22,'Украсть дизайн у Trello','TodoApp','<p><strong>Карточки и вот это все</strong></p>
','2025-01-05 00:49:01',NULL,0);
INSERT INTO "to_do" ("id","title","tag","descr","create_date","close_date","is_complete") VALUES (23,'Создать модуль','TodoApp','Попробовать написать модуль на добавление новых типов сортировки через GUI<br>
Как я делал сортировку по невыполненным(скрывал выполненные), сделать так же, но через интерфейс, чтобы юзеру не надо было писать код, а он мог сам в админке натыкать нужные себе фильтры','2025-01-03 10:29:50',NULL,0);
INSERT INTO "to_do" ("id","title","tag","descr","create_date","close_date","is_complete") VALUES (24,'Составить список предположительных расходов на 2025 год','Finance','В списке должны быть расписаны все расходы, которые я только смогу придумать','2025-01-04 17:10:04','2025-01-04 17:15:09',1);
INSERT INTO "to_do" ("id","title","tag","descr","create_date","close_date","is_complete") VALUES (25,'Расписать расходы по месяцам на 2025 год','Finance','Расписывать нужно абсолютной каждый платеж','2025-01-04 17:10:41','2025-01-04 23:31:54',1);
INSERT INTO "to_do" ("id","title","tag","descr","create_date","close_date","is_complete") VALUES (26,'Создать конверты с целями по расходам на 2025 год','Finance','В сбербанке','2025-01-04 17:10:58','2025-01-04 20:54:52',1);
INSERT INTO "to_do" ("id","title","tag","descr","create_date","close_date","is_complete") VALUES (27,'Сделать форму редактирования текста','TodoApp','Форма нужна для модального окна редактирования задачи, пример формы туть https://richtexteditor.com/Demos/','2025-01-04 21:05:26','2025-01-05 01:11:03',1);
INSERT INTO "to_do" ("id","title","tag","descr","create_date","close_date","is_complete") VALUES (28,'Добавить кнопки изменения статуса в окно просмотра задачи','TodoApp',NULL,'2025-01-05 01:34:02','2025-01-05 01:34:08',1);
INSERT INTO "to_do" ("id","title","tag","descr","create_date","close_date","is_complete") VALUES (29,'Найти хороший плеер для музыки на win/linux','Life','<p>Плеер должен быть:<br />
1. Прост в использовании<br />
2. В идеале иметь версию под андроид<br />
3. Иметь cli-вариант<br />
4. Работать оффлайн<br />
5. Должен ставиться без танцев с бубном<br />
--------------------------------------------------------------<br />
Пока нашел под linux - mocp</p>
','2025-01-05 16:38:17',NULL,0);
INSERT INTO "to_do" ("id","title","tag","descr","create_date","close_date","is_complete") VALUES (30,'*ИДЕЯ* Добавить авторизацию','TodoApp','<p><strong>Для чего:</strong></p>

<ol>
	<li>В системе сможет работать множество пользователей</li>
	<li>Можно будет назначать ответственных к задачам</li>
	<li>Можно будет отправлять уведомления по статусам и обновлениям задач ответственным в тг через бота(хочется реализовать его через pyrogram, чтобы интереснее было)</li>
	<li>Можно будет добавить систему комментариев к задачам внутри проектов</li>
	<li>Можно будет назначать к одной задаче нескольких пользователей</li>
</ol>

<p><strong>Как это будет работать:</strong><br />
&nbsp;</p>
','2025-01-05 03:52:00',NULL,0);
INSERT INTO "to_do" ("id","title","tag","descr","create_date","close_date","is_complete") VALUES (31,'Добавить снежинки на все окна/страницы сайта','TodoApp','<p>Кроме страницы статистики</p>
','2025-01-05 03:39:43','2025-01-09 03:40:36',1);
INSERT INTO "to_do" ("id","title","tag","descr","create_date","close_date","is_complete") VALUES (32,'Тестовая','Life','<p><a href="https://mikrotik.moscow/upload/img-m/image%201.png" target="_parent"><img alt="" src="https://mikrotik.moscow/upload/img-m/image%201.png" /></a>Введите описание задачи</p>
','2025-01-05 03:43:05','2025-01-06 06:47:56',1);
INSERT INTO "to_do" ("id","title","tag","descr","create_date","close_date","is_complete") VALUES (33,'Реализовать поиск по задачам','TodoApp_list','<p>Поиск по ключевым словам без учета регистра</p>
','2025-01-05 03:55:13','2025-01-06 00:35:21',1);
INSERT INTO "to_do" ("id","title","tag","descr","create_date","close_date","is_complete") VALUES (34,'Найти часы','Life','<p>Посмотреть в коробке с железом</p>
','2025-01-05 15:59:49','2025-01-05 16:12:02',1);
INSERT INTO "to_do" ("id","title","tag","descr","create_date","close_date","is_complete") VALUES (35,'*ИДЕЯ* Интегрировать менеджер с ботом в тг','TodoApp','<p>Писать заметки в тг, публиковать их на сервисе<br />
Выводить заметки из сервиса(и тг) в чат с ботом</p>
','2025-01-05 17:14:29',NULL,0);
INSERT INTO "to_do" ("id","title","tag","descr","create_date","close_date","is_complete") VALUES (36,'Сделать страницу документации','TodoApp','<p>Эта страница будет похожа на страницу со списком задач, но будет как бы отдельным проектом со своей админкой и немного измененным функционалом</p>
','2025-01-06 00:32:48',NULL,0);
INSERT INTO "to_do" ("id","title","tag","descr","create_date","close_date","is_complete") VALUES (37,'Переделать меню','TodoApp','<p>Меню должно выглядеть как одна кнопка, при нажатии открывается выпадающий список со всеми нужными кнопками</p>
','2025-01-06 00:35:11','2025-01-07 03:49:31',1);
INSERT INTO "to_do" ("id","title","tag","descr","create_date","close_date","is_complete") VALUES (38,'Переделать страницу статистики','TodoApp','<p>Примерный дизайн накидал в <a href="https://www.figma.com/design/kydT3G7c0ZenrfmFgUV2vx/KOD1.4-Variant3-(Copy)?node-id=0-1&amp;p=f&amp;t=khZwl8GLnTugg9WR-0">Figma</a></p>
','2025-01-06 00:36:11','2025-01-07 03:49:36',1);
INSERT INTO "to_do" ("id","title","tag","descr","create_date","close_date","is_complete") VALUES (39,'Обновить график по статусам задач','TodoApp_stats','<p>Добавить на график статистики по созданию задач граф по статистике выполнения задач</p>
','2025-01-07 18:40:15','2025-01-07 21:08:27',1);
INSERT INTO "to_do" ("id","title","tag","descr","create_date","close_date","is_complete") VALUES (40,'Сделать включение/отключение снега','TodoApp_admin','<p>Оно должно работать через JS и через куки</p>
','2025-01-07 19:02:29','2025-01-07 20:32:15',1);
INSERT INTO "to_do" ("id","title","tag","descr","create_date","close_date","is_complete") VALUES (41,'Тестовая задача от 07.01.2025','Life','<p>Хочу <s><strong><em>потыкаться</em></strong></s> с редактором</p>

<ol>
	<li>один</li>
	<li>два</li>
</ol>

<table align="center" border="1" cellpadding="1" cellspacing="1" style="width:100%" summary="А так можно было?">
	<caption>Ничего себе</caption>
	<tbody>
		<tr>
			<td>1</td>
			<td>банан</td>
		</tr>
		<tr>
			<td>2</td>
			<td>апельсина</td>
		</tr>
		<tr>
			<td>3</td>
			<td>яблока</td>
		</tr>
	</tbody>
</table>

<p>&nbsp;</p>
','2025-01-07 21:35:06','2025-01-08 23:11:34',1);
INSERT INTO "to_do" ("id","title","tag","descr","create_date","close_date","is_complete") VALUES (42,'Добавить приветственную страницу','TodoApp','<p>Описание нововведений и роадмап</p>
','2025-01-08 19:28:47','2025-01-09 03:37:53',1);
INSERT INTO "to_do" ("id","title","tag","descr","create_date","close_date","is_complete") VALUES (43,'*СРОЧНО* Добавить форму обратной связи','TodoApp','<p>Модальное окно, в котором юзер может оставить свое предложение по доработке системы, а так же указать адрес электронной почты(по желанию), куда придет ответ от меня.<br />
<br />
Мне это предложение поступает в личную админку + в тг-бота. В админке я смогу менять статус - отвечено/не отвечено, а через бота буду оперативно получать уведомления о предложениях</p>
','2025-01-08 19:30:57',NULL,0);
INSERT INTO "to_do" ("id","title","tag","descr","create_date","close_date","is_complete") VALUES (44,'Починить положение кнопки меню на странице модальных окон','TodoApp','<p>Там откуда-то берется margin 8, непонятно откуда именно</p>
','2025-01-08 19:48:24','2025-01-08 19:54:30',1);
INSERT INTO "to_do" ("id","title","tag","descr","create_date","close_date","is_complete") VALUES (45,'Добавить функцию создания новостей в админке','TodoApp_admin','<p>Аналогично созданию задачи, но с выводом на about.html</p>
','2025-01-09 03:38:32','2025-01-09 04:52:32',1);
INSERT INTO "to_do" ("id","title","tag","descr","create_date","close_date","is_complete") VALUES (46,'Создать архив с настройками системы','Life','<p>Собрать список конфигов, настроек, плагинов, алиасов, ключей, которые есть в моей системе и которые потребуются после переустановки и залить их в приватную репу на гите</p>
','2025-01-09 04:46:54',NULL,0);
INSERT INTO "to_do" ("id","title","tag","descr","create_date","close_date","is_complete") VALUES (47,'Добавить график на страницу проектов','TodoApp_stats','<p>Если не выбран ни один проект(то есть отправляется get) - отображать статистику создания/закрытия задач по всем проектам сразу</p>
','2025-01-09 04:49:36','2025-01-09 21:24:35',1);
INSERT INTO "to_do" ("id","title","tag","descr","create_date","close_date","is_complete") VALUES (48,'Инвертировать выводимые задачи','TodoApp_list','<p>Вверху списка выводить последние созданные невыполненные задачи</p>
','2025-01-09 20:08:17','2025-01-09 20:08:20',1);
INSERT INTO "to_do" ("id","title","tag","descr","create_date","close_date","is_complete") VALUES (49,'Про тесты','TodoApp','<p>Когда добавлю авторизацию и свяжу ее со всем остальным проектом, нужно будет:<br />
1. Создать форму обратной связи<br />
2. Прикрепить баннер на странице создания аккаунта/создания проектов/создания задач со словами о том, что все созданное в рамках этой тестовой версии может быть утрачено при релизе и если юзер хочет сохранить свои данные, пусть напишет мне</p>
','2025-01-09 22:20:37',NULL,0);
COMMIT;
