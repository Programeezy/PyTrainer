import random
import re
from . import db_methods
from django.shortcuts import render, HttpResponse


def index(request):
    return render(request, 'regulars/index.html')


def get_task(request):
    tasks = db_methods.get_tasks()
    task = random.choice(tasks)
    print(task)
    articles = db_methods.get_articles()
    first_article = articles[0]
    article = ' '.join(first_article[2])
    article_result = eval(task[4])
    context = {'task_id': task[0],
               'status': task[1],
               'task_name': task[2],
               'description': task[3],
               'solution': "def solution(article):\n    # write code here\n    return ''",
               'name': first_article[1],
               'content': first_article[2],
               'article_result': article_result,
               'visibility': 'hidden'}
    if request.method == 'POST':
        solution_code = request.POST['solution_code']
        exec(solution_code, globals())
        context['solution'] = solution_code
        if 'run' in request.POST:
            context['result'] = solution(article)
        elif 'submit' in request.POST:
            articles = db_methods.get_articles()
            for ind, art in enumerate(articles):
                one_article = articles[ind]
                article = ' '.join(one_article[2])
                article_result = eval(task[4])
                if article_result != solution(article):
                    context['failed_test'] = str(ind+1) + '/' + str(len(articles))
                    context['failed_output'] = solution(article)
                    context['right_output'] = article_result
                    context['visibility'] = 'visible'
                    break
            else:
                return HttpResponse('woooow!')
    return render(request, 'regulars/task.html', context=context)


