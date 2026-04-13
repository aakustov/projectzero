from django.shortcuts import render, redirect
from django.http import JsonResponse
from .models import Articles
from django.views.decorators.http import require_GET, require_POST

def start_view(request):
    # Обработка reset
    print(request.session.get)
    request.session.pop('question_count', None)
    request.session.pop('correct_count', None)
    request.session.pop('wrong_count', None)
    request.session.pop('asked_questions', None)
    
    # Инициализация переменных
    request.session['question_count'] = 0
    request.session['correct_count'] = 0
    request.session['wrong_count'] = 0
    request.session['asked_questions'] = []

    return render(request, 'roundone/start.html')
    
def roundone(request):
    return render(request, 'roundone/roundone.html', {'title': 'Первый раунд'})

@require_GET
def next_question(request):
    # Получаем список уже заданных вопросов из сессии
    asked_questions = request.session.get('asked_questions', [])
    
    # Получаем вопрос, которого ещё не было
    question = Articles.objects.exclude(id__in=asked_questions).order_by('?').first()
    
    if not question:
        # Все вопросы заданы, возвращаем ошибку или сообщение
        return JsonResponse({'error': 'Все вопросы пройдены'})
    
    # Добавляем текущий вопрос в список уже заданных
    asked_questions.append(question.id)
    request.session['asked_questions'] = asked_questions
    
    # Возвращаем вопрос
    return JsonResponse({
        'question': question.question,
        'answer': question.answer,
        'variant_1': question.variant_1,
        'variant_2': question.variant_2,
        'variant_3': question.variant_3,
        'variant_4': question.variant_4,
        'question_id': question.id,
    })

@require_POST
def answer_question(request):
    user_answer = request.POST.get('answer')  # ответ пользователя
    question_id = request.POST.get('question_id')
    try:
        question = Articles.objects.get(id=question_id)
    except Articles.DoesNotExist:
        return JsonResponse({'error': 'Вопрос не найден'})

    # Получение счетчиков из сессии
    question_count = request.session.get('question_count', 0)
    correct_count = request.session.get('correct_count', 0)
    wrong_count = request.session.get('wrong_count', 0)

    question_count += 1

    # Проверка правильности ответа
    if user_answer == question.answer:
        correct_count += 1
        is_correct = True
    else:
        wrong_count += 1
        is_correct = False

    # Обновляем счетчики в сессии
    request.session['question_count'] = question_count
    request.session['correct_count'] = correct_count
    request.session['wrong_count'] = wrong_count

    # Проверка на завершение игры
    if question_count >= 20:
        return JsonResponse({'finish': True})
    else:
        return JsonResponse({'correct': is_correct})

def result_view(request):
    question_count = request.session.get('question_count', 0)
    correct_count = request.session.get('correct_count', 0)
    wrong_count = request.session.get('wrong_count', 0)

    # сбрасываем счетчики
    request.session['question_count'] = 0
    request.session['correct_count'] = 0
    request.session['wrong_count'] = 0

    return render(request, 'roundone/result.html', {
        'question_count': question_count,
        'correct_count': correct_count,
        'wrong_count': wrong_count,
    })