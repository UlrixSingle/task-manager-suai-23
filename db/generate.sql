--- Удаление информации предыдущей базы данных ---
DROP TABLE IF EXISTS "system_role";
DROP TABLE IF EXISTS "user";
DROP TABLE IF EXISTS "project";
DROP TABLE IF EXISTS "role";
DROP TABLE IF EXISTS "team";
DROP TABLE IF EXISTS "stage";
DROP TABLE IF EXISTS "priority";
DROP TABLE IF EXISTS "task";
DROP TABLE IF EXISTS "comment";
DROP TABLE IF EXISTS "announce";
--- DROP DATABASE IF EXISTS "db"; ---

--- Создание и заполнение таблицы Системная роль ---
CREATE TABLE "system_role" (
    "system_role_id" integer NOT NULL GENERATED ALWAYS AS IDENTITY,
    "name" varchar(32) NOT NULL,
    
    CONSTRAINT "system_role_pk" PRIMARY KEY ("system_role_id"),
    CONSTRAINT "system_role_unique_name" UNIQUE ("name")
);

INSERT INTO "system_role" ("name") VALUES
	 ('Администратор'),
	 ('Пользователь');


--- Создание и заполнение таблицы Пользователь ---
CREATE TABLE "user" (
    "user_id" integer NOT NULL GENERATED ALWAYS AS IDENTITY,
    "login" varchar(20) NOT NULL,
    "password" varchar(64),
    "nickname" varchar(20) NOT NULL,
    "second_name" varchar(20),
    "first_name" varchar(20),
    "surname" varchar(20),
    "descr" varchar(600),
    "mail" varchar(32),
    "phone" varchar(32),
    "system_role_id" integer DEFAULT 2 NOT NULL,
    
    CONSTRAINT "user_pk" PRIMARY KEY ("user_id"),
    CONSTRAINT "user_unique_login" UNIQUE ("login"),
    CONSTRAINT "user_unique_nickname" UNIQUE ("nickname"),
    CONSTRAINT "user_fk_system_role_id" FOREIGN KEY ("system_role_id") REFERENCES "system_role" ("system_role_id") ON UPDATE CASCADE
);

INSERT INTO "user" ("login", "password", "nickname", "second_name", "first_name", "surname", "descr", "mail", "phone", "system_role_id") VALUES
	 ('user1','passuser1','TimBL','Бернерс-Ли','Тим','Конвей','Люблю мировую паутину',NULL,NULL,2),
	 ('user2','passuser2','Knot','Кнут','Дональд',NULL,'Учу искусству программирования по всему миру',NULL,NULL,2),
	 ('user3','passuser3','DoomGuy','Кармак','Джон','Стэн','Создаю известные игры. Джону Ромеро передавайте привет!',NULL,NULL,2),
	 ('user4','passuser4','Builder','Пажитнов','Алексей','Леонидович','Ну ладно, дам поиграть в Tetris со своего телефона',NULL,NULL,2),
	 ('admin1','passadmin1','Gendalf','Торвальдс','Линус','Нильс','Люблю пингвинов',NULL,NULL,1);


--- Создание и заполнение таблицы Проект ---
CREATE TABLE "project" (
    "project_id" integer NOT NULL GENERATED ALWAYS AS IDENTITY,
    "name" varchar(32) NOT NULL,
    "descr" varchar(600),
    "task_number" integer DEFAULT 0 NOT NULL,
    "user_number" integer DEFAULT 0 NOT NULL,
    
    CONSTRAINT "project_pk" PRIMARY KEY ("project_id"),
    CONSTRAINT "project_unique_name" UNIQUE ("name")
);

INSERT INTO "project" ("name",descr,task_number,user_number) VALUES
	 ('Радиоуправляемая машинка','Модель машины на радиоуправлении',0,3);


--- Создание и заполнение таблицы Роль (члена команды в проекте) ---
CREATE TABLE "role" (
    role_id integer NOT NULL GENERATED ALWAYS AS IDENTITY,
    name varchar(32) NOT NULL,
    
    CONSTRAINT "role_pk" PRIMARY KEY ("role_id"),
    CONSTRAINT "role_unique_name" UNIQUE ("name")
);

INSERT INTO "role" ("name") VALUES
	 ('Руководитель проекта'),
	 ('Участник проекта'),
	 ('Гость');


--- Создание и заполнение таблицы Команды проектов ---
CREATE TABLE "team" (
    "user_id" integer NOT NULL,
    "project_id" integer NOT NULL,
    "role_id" integer NOT NULL,
    "job" varchar(32),
    
    CONSTRAINT "team_pk" PRIMARY KEY ("role_id"),
    CONSTRAINT "team_fk_user_id" FOREIGN KEY ("user_id") REFERENCES "user" ("user_id") ON DELETE CASCADE ON UPDATE CASCADE,
    CONSTRAINT "team_fk_project_id" FOREIGN KEY ("project_id") REFERENCES "project" ("project_id") ON DELETE CASCADE ON UPDATE CASCADE
);

INSERT INTO "team" ("user_id", "project_id", "role_id", "job") VALUES
	 (1,1,1,'Программист'),
	 (2,1,2,'Инженер'),
	 (3,1,3,NULL);

 
--- Создание и заполнение таблицы Этап выполнения (для задачи) ---
CREATE TABLE "stage" (
    "stage_id" integer NOT NULL GENERATED ALWAYS AS IDENTITY,
    "name" varchar(20) NOT NULL,
    
    CONSTRAINT "stage_pk" PRIMARY KEY ("stage_id"),
    CONSTRAINT "stage_unique_name" UNIQUE ("name")
);

INSERT INTO "stage" ("name") VALUES
	 ('Предстоит сделать'),
	 ('Анализ'),
	 ('В работе'),
	 ('На рассмотрении'),
	 ('Готово');


--- Создание и заполнение таблицы Приоритет (для задачи) ---
CREATE TABLE "priority" (
    "priority_id" integer NOT NULL GENERATED ALWAYS AS IDENTITY,
    "name" varchar(20) NOT NULL,
    "colour" varchar(20),
    "weight" integer DEFAULT 0 NOT NULL,
    
    CONSTRAINT "priority_pk" PRIMARY KEY ("priority_id"),
    CONSTRAINT "priority_unique_name" UNIQUE ("name")
);

INSERT INTO "priority" ("name", "colour", "weight") VALUES
	 ('Незначительная','#e6e6e6',0),
	 ('Средняя','#e6f6cf',-1),
	 ('Серьезная','#ffee9c',-2),
	 ('Ключевая','#ffc8ea',-3),
	 ('Критическая','#E30000',-4);


--- Создание и заполнение таблицы Задача ---
CREATE TABLE "task" (
    "task_id" integer NOT NULL GENERATED ALWAYS AS IDENTITY,
    "project_id" integer NOT NULL,
    "name" varchar(64) NOT NULL,
    "descr" varchar(600),
    "begindate" date,
    "enddate" date,
    "stage_id" integer DEFAULT 1 NOT NULL,
    "priority_id" integer DEFAULT 1 NOT NULL,
    "type" varchar(32),
    "field" varchar(32),
    "user_id" integer DEFAULT 0,
    
    CONSTRAINT "task_pk" PRIMARY KEY ("task_id"),
    CONSTRAINT "task_fk_project_id" FOREIGN KEY ("project_id") REFERENCES "project" ("project_id") ON DELETE CASCADE ON UPDATE CASCADE,
    CONSTRAINT "task_fk_stage_id" FOREIGN KEY ("stage_id") REFERENCES "stage" ("stage_id") ON UPDATE CASCADE,
    CONSTRAINT "task_fk_priority_id" FOREIGN KEY ("priority_id") REFERENCES "priority" ("priority_id") ON UPDATE CASCADE
);

INSERT INTO "task" ("project_id", "name", "descr", "begindate", "enddate", "stage_id", "priority_id", "type", "field", "user_id") VALUES
	 (1,'Корпус','Собрать корпус',NULL,NULL,4,2,NULL,'Инженерия',NULL),
	 (1,'Колеса','Подобрать хорошие колеса',NULL,NULL,3,2,NULL,'Закупки',NULL),
	 (1,'Мотор','Подобрать быстрый и достаточно мощный двигатель. Лучше всего будет, если он еще не будет занимать много места',NULL,NULL,2,2,NULL,'Закупки',NULL),
	 (1,'Контроллер и пульт','Подобрать систему радиоуправления',NULL,NULL,1,1,NULL,'Закупки',NULL),
	 (1,'Схема','',NULL,NULL,5,3,'Планирование','',1);


--- Создание и заполнение таблицы Комментарий (к задаче) ---
CREATE TABLE "comment" (
    "comment_id" integer NOT NULL GENERATED ALWAYS AS IDENTITY,
    "task_id" integer NOT NULL,
    "user_id" integer NOT NULL,
    "postdate" date NOT NULL,
    "descr" varchar(600),
    
    CONSTRAINT "comment_pk" PRIMARY KEY ("comment_id"),
    CONSTRAINT "comment_fk_task_id" FOREIGN KEY ("task_id") REFERENCES "task" ("task_id") ON DELETE CASCADE ON UPDATE CASCADE,
    CONSTRAINT "comment_fk_user_id" FOREIGN KEY ("user_id") REFERENCES "user" ("user_id") ON DELETE CASCADE ON UPDATE CASCADE
);

INSERT INTO "comment" ("task_id", "user_id", "postdate", "descr") VALUES
	 (1,2,'2024-01-12','Почему не в виде гоночной?'),
	 (1,1,'2024-01-12','Звучит неплохо. Давайте делать грузовик'),
	 (1,2,'2024-01-12','Хорошо, я тоже согласен'),
	 (1,3,'2024-01-12','Может тогда сделаете грузовик? Он, конечно, не быстрый, но зато можно будет уместить много дополнительных элементов'),
	 (1,1,'2024-01-12','Думаю сделать ее в виде пожарной машины'),
	 (1,1,'2024-01-12','Потому что на гоночную машину кроме камеры что-то тяжело будет прицепить');
 
 
--- Создание и заполнение таблицы Обьявление ---
CREATE TABLE "announce" (
    "announce_id" integer NOT NULL GENERATED ALWAYS AS IDENTITY,
    "postdate" date NOT NULL,
    "descr" varchar(600) NOT NULL,
    "user_id" integer NOT NULL,
    
    CONSTRAINT "announce_pk" PRIMARY KEY ("announce_id")
);
