INSERT INTO Task_log (User, Task, Name, Description, Solution, Date)
VALUES ("%d", "%d", "%s", "%s", "%s", "%(date)s");

INSERT INTO Article_log (User, Article, Name, Content, Date)
VALUES ("%d", "%d", "%s", "%s", "%(date)s");


-- Find tasks by user --
SELECT * 
FROM Task_log
WHERE User = "%d";

-- Select task --
SELECT *
FROM Task_log
WHERE Task = "%d";

-- Select task by date --
SELECT *
FROM Task_log
WHERE Task = "%d" AND Date = "%(date)s";



-- Find articles by user --
SELECT *
FROM Article_log
WHERE User = "%d";

-- Select article --
SELECT *
FROM Article_log
WHERE Article = "%d"

-- Select article by date --
SELECT *
FROM Article_log
WHERE Article = "%d" AND Date = "%(date)s"