<h1>RU</h1>

<h3>Бот опросник</h3>

<p>Telegram бот -Python 3.9 Telebot/MatPotLib </p>

<ul> <h5>Библиотеки</h5>
  <li>Telebot</li>
  <li>MatPotLib</li>
</ul>
<p> Бот собирает информацию с пользователей. Администратор может получать данные в виде диаграмм. </p> 
<h4>Таблицы базы данных</h4>
<h5> Администраторы </h5>
<i>CREATE TABLE `admins` (<br>
  `t_id` bigint DEFAULT NULL<br>
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
</i>
<h5>Ответы на опрос</h5>
<i>
  CREATE TABLE `poll_req` (<br>
  `id` int NOT NULL AUTO_INCREMENT COMMENT 'ID',<br>
  `poll_id` int DEFAULT NULL COMMENT 'id опроса',<br>
  `Answers` text COLLATE utf8mb4_bin COMMENT 'Ответы на опрос',<br>
  `t_id` bigint DEFAULT NULL,<br>
  `Date` date DEFAULT NULL,<br>
  PRIMARY KEY (`id`)<br>
) ENGINE=InnoDB AUTO_INCREMENT=33 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin;
</i>
<h5> Опросы </h5>
<i>
  CREATE TABLE `polls` ( <br>
  `id` int NOT NULL AUTO_INCREMENT COMMENT 'id',<br>
  `name` varchar(30) DEFAULT NULL,<br>
  `t_id` bigint DEFAULT NULL,<br>
  `Questions` text COMMENT 'Вопросы',<br>
  `cols` int DEFAULT NULL COMMENT 'Сколько людей ответило',<br>
  `show` int DEFAULT '0',<br>
  `Date` date DEFAULT NULL,<br>
  PRIMARY KEY (`id`)<br>
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
  </i>
<img src='example.png'>
<br>
<br>
<h1>EN</h1>

<h3>Poll bot</h3>

<p>Telegram bot -Python 3.9 Telebot/MatPotLib </p>

<ul> <h5>Libraries</h5>
  <li>Telebot</li>
  <li>MatPotLib</li>
</ul>
<p> Bot collect information from users. Admin can get information as diagram. </p> 
<h4>Database tables</h4>
<h5> Admins </h5>
<i>CREATE TABLE `admins` (<br>
  `t_id` bigint DEFAULT NULL<br>
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
</i>
<h5>Polls answers</h5>
<i>
  CREATE TABLE `poll_req` (<br>
  `id` int NOT NULL AUTO_INCREMENT COMMENT 'ID',<br>
  `poll_id` int DEFAULT NULL COMMENT 'poll id',<br>
  `Answers` text COLLATE utf8mb4_bin COMMENT 'poll answers',<br>
  `t_id` bigint DEFAULT NULL,<br>
  `Date` date DEFAULT NULL,<br>
  PRIMARY KEY (`id`)<br>
) ENGINE=InnoDB AUTO_INCREMENT=33 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin;
</i>
<h5> Polls </h5>
<i>
  CREATE TABLE `polls` ( <br>
  `id` int NOT NULL AUTO_INCREMENT COMMENT 'id',<br>
  `name` varchar(30) DEFAULT NULL,<br>
  `t_id` bigint DEFAULT NULL,<br>
  `Questions` text COMMENT 'Polls questions',<br>
  `cols` int DEFAULT NULL COMMENT 'how many people answered',<br>
  `show` int DEFAULT '0',<br>
  `Date` date DEFAULT NULL,<br>
  PRIMARY KEY (`id`)<br>
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
  </i>
<img src='example.png'>
