import psycopg2
import random
import re
from django.shortcuts import render, HttpResponse


def index(request):
    return render(request, 'regulars/index.html')


def get_task(request):
    conn = psycopg2.connect("dbname=django_db user=anton password=3ie8 host=127.0.0.1")
    cur = conn.cursor()

    cur.execute('SELECT * FROM task')
    tasks = cur.fetchall()
    task = random.choice(tasks)
    cur.execute('SELECT * FROM article')
    articles = cur.fetchall()
    first_article = articles[0]
    article = ' '.join(first_article[2])
    article_result = eval(task[3])
    context = {'task_id': task[0],
               'status': task[1],
               'description': task[2],
               'solution': "def solution(article):\n    # write code here\n    return ''",
               'name': first_article[1],
               'content': first_article[2],
               'article_result': article_result}
    if request.method == 'POST':
        solution_code = request.POST['solution_code']
        exec(solution_code, globals())
        context['result'] = solution(article)
        context['solution'] = solution_code
    return render(request, 'regulars/task.html', context=context)
