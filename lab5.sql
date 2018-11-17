SELECT *
FROM User
WHERE Role = '%d';

SELECT * FROM Level;

SELECT * FROM Article;

SELECT *
FROM Article
WHERE Article.Author = '%s';


SELECT * FROM Task;

SELECT *
FROM Task
WHERE Task.Level >= '%d';


SELECT * FROM Level;

SELECT *
FROM Task
WHERE User = (
    SELECT T_s.User
    FROM Task_status T_s
    WHERE T_s.Status = '%s'
    );
