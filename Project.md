
# PyTrainer
Приложение, помогающее в обучении и запоминании информации

## Сущности

### User
	1. Id
	2. Name
	3. E-mail
	4. Password
	5. Level(Id)
	6. Experience
	7. Role(FK Role(Id))

### Role
	1. Id
	2. Name

### Level
	1. Id
	2. Experience_required

### Task
	1. Id
	2. Name
	3. Description
	4. Experience_award
	5. Level_required(FK Level(Id))
	6. Solution
	7. Creator(FK User(Id))

### Article
	1. Id
	2. Name
	3. Content
	4. Author(FK User(Id))

### Task_status
	1. User (pk, FK User(Id))
	2. Task (pk, FK Task(Id))
	3. Status
	4. Attempts

### Article_log
	1. Article_id (pk, FK Article(Id))
	2. User_id (pk, FK User(Id))
	3. Name
	4. Description
	5. Date

### Task_log
	1. Task_id (pk, FK Task(Id))
	2. User_id (pk, FK User(Id))
	3. Name
	4. Description
	5. Solution
	6. Date
	
## Функции
	1. Авторизация пользователей
	2. Создание, удаление пользователей
	3. Запись о решенных задачах в таблицу Task_status
	4. Добавление, изменение и удаление задач администраторами.
	5. Добавление, изменение и удаление статей администраторами.
	6. Увеличение опыта пользователей при решении задач.
	7. Увеличение уровня пользователей при достижении необходимого количества опыта.
