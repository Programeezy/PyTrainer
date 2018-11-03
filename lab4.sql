INSERT INTO Role (Name)
VALUES(%s);

INSERT INTO Level (Experience_required)
VALUES (%d);

INSERT INTO User (Name, Password, Level, Role)
VALUES (%s, %s, %d, %d);

INSERT INTO Task (Name , Description, Experience_award, Solution, Creator)
VALUES (%s, %s, %d, %s, %d);

INSERT INTO Article (Name, Content , Author)
VALUES (%s, %s, %d);

INSERT INTO Task_status (User, Task, Status, Attempts)
VALUES (%d, %d, %s, %d);

UPDATE Task_status SET Status = %s, Attempts = %d WHERE Id = %d;