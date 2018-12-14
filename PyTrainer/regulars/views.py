import random
import re
from . import db_methods
from django.shortcuts import render, redirect, HttpResponse


def main(request):
    context = {'user_name': db_methods.find_active()}
    return render(request, 'regulars/main_page.html', context=context)


def get_task(request):
    print(db_methods.find_active())
    tasks = db_methods.get_tasks()
    task = tasks[0]
    articles = db_methods.get_articles()
    len_articles = len(articles)
    first_article = articles[-1]
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
               'visibility': 'hidden',
               'user_name': db_methods.find_active()}
    if request.method == 'POST':
        solution_code = request.POST['solution_code']
        context['solution'] = solution_code
        try:
            exec(solution_code, globals())
            context['result'] = solution(article)
        except Exception as e:
            context['result'] = e
            return render(request, 'regulars/task.html', context=context)
        if 'submit' in request.POST:
            articles = db_methods.get_articles()[::-1]
            for ind, art in enumerate(articles):
                one_article = articles[ind]
                article = ' '.join(one_article[2])
                article_result = eval(task[4])
                if article_result != solution(article):
                    wrong_test = str(ind+1) + '/' + str(len_articles)
                    context['failed_test'] = wrong_test
                    context['failed_output'] = solution(article)
                    context['right_output'] = article_result
                    context['visibility'] = 'visible'
                    db_methods.add_attempt(task[0], task[2], 'wrong', wrong_test)
                    break
            else:
                db_methods.add_attempt(task[0], task[2], 'correct', str(len_articles) + '/' + str(len_articles))
                return redirect('history')
    return render(request, 'regulars/task.html', context=context)


def show_history(request):
    attempts = db_methods.get_attempts()
    len_articles = len(db_methods.get_articles())
    filtered_attempts = list()
    for attempt in attempts:
        filtered_attempts.append({'id': attempt[0],
                                  'task_name': attempt[2],
                                  'solution': attempt[3],
                                  'passed_tests': attempt[4],
                                  'date': attempt[5],
                                  'color': 'table-danger' if bool(attempt[4].split('/')[0] != str(len_articles))
                                  else 'table-success'})
    context = {'attempts': filtered_attempts, 'user_name': db_methods.find_active()}
    return render(request, 'regulars/history.html', context=context)


def show_tasks(request):
    tasks = db_methods.get_tasks()
    dict_tasks = []
    for task in tasks:
        dict_tasks.append({'id': task[0],
                           'status': task[1],
                           'name': task[2],
                           'solution': task[4]})
    context = {'tasks': dict_tasks, 'user_name': db_methods.find_active()}
    return render(request, 'regulars/tasks.html', context=context)


def show_articles(request):
    articles = db_methods.get_articles()
    dict_articles = []
    for article in articles:
        dict_articles.append({'id': article[0],
                              'name': article[1]})
    context = {'articles': dict_articles, 'user_name': db_methods.find_active()}
    return render(request, 'regulars/articles.html', context=context)


def show_actions(request):
    dict_actions = []
    attempts = db_methods.get_attempts()
    for attempt in attempts:
        dict_actions.append({'type': 'attempt',
                             'process': 'submit',
                             'name': attempt[2],
                             'date': attempt[5]})
    article_logs = db_methods.get_article_logs()
    for article_log in article_logs:
        dict_actions.append({'type': 'article_log',
                             'process': article_log[4],
                             'name': article_log[2],
                             'date': article_log[5]})
    task_logs = db_methods.get_task_logs()
    for task_log in task_logs:
        dict_actions.append({'type': 'task_log',
                             'process': task_log[5],
                             'name': task_log[2],
                             'date': task_log[6]})
    context = {'actions': sorted(dict_actions, key=lambda k: k['date'], reverse=True),
               'user_name': db_methods.find_active()}
    return render(request, 'regulars/actions.html', context=context)


def login(request):
    users = db_methods.get_users()
    if users:
        if request.method == 'POST' and 'sign_in' in request.POST:
            username = request.POST['username']
            password = request.POST['password']
            context = {'username': username}
            for user in users:
                if username == user[1]:
                    if password == user[2]:
                        db_methods.set_user_activity(username, True)
                        print(db_methods.find_active())
                        return redirect('main')
                    else: # сделать красивое подсвечивание, что пароль неверный
                        return render(request, 'registration/login.html', context=context)
    else:
        return redirect('register')
    return render(request, 'registration/login.html')


def register(request):
    users = db_methods.get_users()
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        password_ident = request.POST['password_ident']
        key = request.POST['key']
        for user in users:
            if username == user[1]: # сделать красивое подсвечивание, что пароль неверный
                return render(request, 'registration/register.html')
        else:
            if password == password_ident and password:
                if key:
                    for user in users:
                        if key == user[4]:
                            db_methods.add_user(username, password, 'superuser')
                            return redirect('main')
                else:
                    db_methods.add_user(username, password)
                    return redirect('main')
    return render(request, 'registration/register.html') # сделать красивое подсвечивание,чт ключ неверный


def logout(request):
    active_user_name = db_methods.find_active()
    db_methods.set_user_activity(active_user_name, False)
    return redirect('main')
