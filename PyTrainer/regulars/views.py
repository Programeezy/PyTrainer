import re
from . import db_methods
from django.shortcuts import render, redirect, HttpResponse
from django.http import JsonResponse


def main(request):
    db_methods.attempt_admin()
    context = {'user_name': db_methods.find_active(request.COOKIES), 'empty_page': True}
    return render(request, 'regulars/main_page.html', context=context)


def get_task(request):
    if db_methods.find_active(request.COOKIES):
        tasks = db_methods.get_tasks(request.COOKIES)
        if not tasks:
            db_methods.fill_tasks(request.COOKIES)

        articles = db_methods.get_articles(request.COOKIES)
        if not articles:
            db_methods.fill_articles(request.COOKIES)

        tasks = db_methods.get_tasks(request.COOKIES)
        for unknown_task in tasks:
            if unknown_task[1] == 'unsolved':
                return redirect('solve_task', task_id=unknown_task[0])
        return redirect('tasks')
    else:
        return redirect('main')


def solve_task(request, task_id):
    if db_methods.find_active(request.COOKIES):
        tasks = db_methods.get_tasks(request.COOKIES)
        task = ''
        for unknown_task in tasks:
            if unknown_task[0] == task_id:
                task = unknown_task
        articles = db_methods.get_articles(request.COOKIES)
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
                   'user_name': db_methods.find_active(request.COOKIES)}
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
                articles = db_methods.get_articles(request.COOKIES)[::-1]
                for ind, art in enumerate(articles):
                    one_article = articles[ind]
                    article = ' '.join(one_article[2])
                    article_result = eval(task[4])
                    if article_result != solution(article):
                        wrong_test = str(ind + 1) + '/' + str(len_articles)
                        context['failed_test'] = wrong_test
                        context['failed_output'] = solution(article)
                        context['right_output'] = article_result
                        context['visibility'] = 'visible'
                        db_methods.add_attempt(request.COOKIES, task[0], task[2], 'wrong', wrong_test)
                        break
                else:
                    db_methods.update_task_status(request.COOKIES, task[0])
                    db_methods.add_attempt(request.COOKIES, task[0], task[2], 'correct',
                                           str(len_articles) + '/' + str(len_articles))
                    return redirect('history')
        return render(request, 'regulars/task.html', context=context)
    else:
        redirect('main')


def show_history(request):
    if db_methods.find_active(request.COOKIES):
        attempts = db_methods.get_attempts(request.COOKIES)
        len_articles = len(db_methods.get_articles(request.COOKIES))
        filtered_attempts = list()
        for attempt in attempts:
            filtered_attempts.append({'id': attempt[0],
                                      'task_name': attempt[3],
                                      'solution': attempt[4],
                                      'passed_tests': attempt[5],
                                      'date': attempt[6],
                                      'color': 'table-danger' if bool(attempt[5].split('/')[0] != str(len_articles))
                                      else 'table-success'})
        context = {'attempts': filtered_attempts, 'user_name': db_methods.find_active(request.COOKIES)}
        return render(request, 'regulars/history.html', context=context)
    else:
        return redirect('main')


def show_tasks(request):
    if db_methods.find_active(request.COOKIES):
        tasks = db_methods.get_tasks(request.COOKIES)
        dict_tasks = []
        active_user = db_methods.find_active(request.COOKIES)
        for task in tasks:
            dict_tasks.append({'id': task[0],
                               'status': task[1],
                               'name': task[2],
                               'solution': task[4] if active_user == 'admin' else 'hidden'})
        context = {'tasks': dict_tasks, 'user_name': db_methods.find_active(request.COOKIES)}
        return render(request, 'regulars/tasks.html', context=context)
    else:
        return redirect('main')


def show_articles(request):
    if db_methods.find_active(request.COOKIES):
        articles = db_methods.get_articles(request.COOKIES)
        dict_articles = []
        for article in articles:
            dict_articles.append({'id': article[0],
                                  'name': article[1]})
        context = {'articles': dict_articles, 'user_name': db_methods.find_active(request.COOKIES)}
        return render(request, 'regulars/articles.html', context=context)
    else:
        return redirect('main')


def show_actions(request):
    if db_methods.find_active(request.COOKIES):
        dict_actions = []
        attempts = db_methods.get_attempts(request.COOKIES)
        for attempt in attempts:
            dict_actions.append({'type': 'attempt',
                                 'process': 'submit',
                                 'name': attempt[3],
                                 'date': attempt[6]})
        article_logs = db_methods.get_article_logs(request.COOKIES)
        for article_log in article_logs:
            dict_actions.append({'type': 'article_log',
                                 'process': article_log[4],
                                 'name': article_log[2],
                                 'date': article_log[5]})
        task_logs = db_methods.get_task_logs(request.COOKIES)
        for task_log in task_logs:
            dict_actions.append({'type': 'task_log',
                                 'process': task_log[5],
                                 'name': task_log[2],
                                 'date': task_log[6]})
        context = {'actions': sorted(dict_actions, key=lambda k: k['date'], reverse=True),
                   'user_name': db_methods.find_active(request.COOKIES)}
        return render(request, 'regulars/actions.html', context=context)
    else:
        return redirect('main')


def login(request):
    if not db_methods.find_active(request.COOKIES):
        users = db_methods.get_users()
        if users:
            if request.method == 'POST' and 'sign_in' in request.POST:
                username = request.POST['username']
                password = request.POST['password']
                context = {'username': username}
                for user in users:
                    if username == user[1]:
                        if password == user[2]:
                            db_methods.add_session(user[0])
                            cookie = db_methods.get_session(user[0])
                            context = {'user_name': username, 'empty_page': True}
                            response = render(request, 'regulars/main_page.html', context=context)
                            response.set_cookie(str(cookie).lower(), 1)
                            print(cookie)
                            return response
                        else:
                            return render(request, 'registration/login.html', context=context)
            elif 'sign_up' in request.POST:
                return redirect('register')
        else:
            return redirect('register')
        return render(request, 'registration/login.html')
    else:
        return redirect('main')


def register(request):
    if not db_methods.find_active(request.COOKIES):
        users = db_methods.get_users()
        if request.method == 'POST':
            username = request.POST['username']
            password = request.POST['password']
            password_ident = request.POST['password_ident']
            key = request.POST['key']
            for user in users:
                if username == user[1]:
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
        return render(request, 'registration/register.html')
    else:
        return redirect('main')


def check_login(request):
    print(request.method)
    is_exist = False
    if request.method == 'POST':
        user_login = request.POST['user_login']
        if user_login:
            users = db_methods.get_users()
            for user in users:
                if user[1] == user_login:
                    is_exist = True
                    break
    context = {'is_exist': is_exist}
    return JsonResponse(context)


def logout(request):
    active_user_id = db_methods.get_active_user_id(request.COOKIES)
    if active_user_id:
        db_methods.delete_session(active_user_id)
    return redirect('main')


def delete_user(request):
    active_user_name = db_methods.find_active(request.COOKIES)
    if active_user_name:
        db_methods.delete_user(active_user_name)
    return redirect('main')
