import random
from django.shortcuts import render
from django.http import JsonResponse
from .models import Articles, GameRecord
from django.views.decorators.http import require_GET, require_POST
from django.views.decorators.csrf import ensure_csrf_cookie
import time

ROUND_LIMIT = 20

@ensure_csrf_cookie
def start_view(request):
    # Инициализация сессии для нового раунда
    request.session['question_count'] = 0
    request.session['correct_count'] = 0
    request.session['wrong_count'] = 0
    request.session['asked_questions'] = []
    request.session.modified = True
    return render(request, 'roundone/start.html')

def roundtwo(request):

    start = time.time()
    # Проверяем, пришел ли флаг сброса
    if request.GET.get('reset') == '1':
        # Обнуляем сессию (копируем логику из start_view)
        request.session['question_count'] = 0
        request.session['correct_count'] = 0
        request.session['wrong_count'] = 0
        request.session['asked_questions'] = []
        request.session.modified = True
        # Опционально: можно сделать редирект, чтобы убрать ?reset=1 из URL
        # from django.shortcuts import redirect
        # return redirect('roundone') 
    print(f"Execution time: {time.time() - start}")

    return render(request, 'roundone/roundone.html', {'title': 'Первый раунд'})


@require_GET
def next_question(request):
    asked_questions = request.session.get('asked_questions', [])
    
    if len(asked_questions) >= ROUND_LIMIT:
        return JsonResponse({'finish': True})
    
    # Оптимизированный выбор: исключаем уже заданные ID
    ids = list(Articles.objects.exclude(id__in=asked_questions).values_list('id', flat=True))
    
    if not ids:
        return JsonResponse({'finish': True})
    
    q_id = random.choice(ids)
    # Сразу берем объект. В идеале здесь можно использовать .values(), 
    # если не нужны методы модели, чтобы было еще быстрее.
    question = Articles.objects.get(id=q_id)
    
    asked_questions.append(question.id)
    request.session['asked_questions'] = asked_questions
    request.session.modified = True
    
    return JsonResponse({
        'question': question.question,
        'variant_1': question.variant_1,
        'variant_2': question.variant_2,
        'variant_3': question.variant_3,
        'variant_4': question.variant_4,
        'question_id': question.id,
        'progress': {
            'current': len(asked_questions),
            'total': ROUND_LIMIT
        }
    })

@require_POST
def answer_question(request):
    user_answer = request.POST.get('answer')
    question_id = request.POST.get('question_id')
    
    if not question_id or user_answer is None:
        return JsonResponse({'error': 'Некорректные данные'}, status=400)

    try:
        question = Articles.objects.get(id=question_id)
    except Articles.DoesNotExist:
        return JsonResponse({'error': 'Вопрос не найден'}, status=404)

    is_correct = (str(user_answer).strip() == str(question.answer).strip())
    
    # Обновляем счетчики в сессии
    request.session['question_count'] = request.session.get('question_count', 0) + 1
    if is_correct:
        request.session['correct_count'] = request.session.get('correct_count', 0) + 1
    else:
        request.session['wrong_count'] = request.session.get('wrong_count', 0) + 1
    
    request.session.modified = True
    is_finished = request.session['question_count'] >= ROUND_LIMIT
    
    return JsonResponse({
        'correct': is_correct,
        'correct_answer': question.answer, 
        'finish': is_finished,
        'stats': {
            'question_count': request.session['question_count'],
            'correct_count': request.session['correct_count'],
            'wrong_count': request.session['wrong_count'],
            'total_limit': ROUND_LIMIT
        }
    })

def result_view(request):
    correct = request.session.get('correct_count', 0)
    total = request.session.get('question_count', 0)
    wrong = request.session.get('wrong_count', 0)

    # Сохраняем результат только если была игра
    if total > 0:
        GameRecord.objects.create(correct_answers=correct, total_questions=total)
        
        # ОЧИСТКА: обнуляем данные сессии после сохранения в БД, 
        # чтобы F5 не создавал новые записи с тем же счетом
        request.session['question_count'] = 0
        request.session['correct_count'] = 0
        request.session['wrong_count'] = 0
        request.session['asked_questions'] = []
        request.session.modified = True
    
    context = {
        'correct_count': correct,
        'question_count': total,
        'wrong_count': wrong,
    }
    return render(request, 'roundone/result.html', context)

def leaderboard_view(request):
    # Сортировка: сначала по кол-ву верных (DESC), затем по общему кол-ву вопросов (ASC)
    top_records = GameRecord.objects.order_by('-correct_answers', 'total_questions')[:10]
    return render(request, 'roundone/leaderboard.html', {'records': top_records})
