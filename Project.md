
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
	7. Role

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
	5. Level_required
	6. Solution
	7. Creator

### Article
	1. Id
	2. Name
	3. Content
	4. Author 

### Task_status
	1. User (pk)
	2. Task (pk)
	3. Status

## Функции
	1. Авторизация пользователей
	2. Создание, удаление пользователей
	3. Запись о решенных задачах в таблицу Task_status
	4. Добавление, изменение и удаление задач администраторами.
	5. Добавление, изменение и удаление стаей администраторами.
	6. Увеличение опыта пользователей при решении задач.
	7. Увеличение уровня пользователей при достижении необходимого количества опыта.
