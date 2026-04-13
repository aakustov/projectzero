from django.contrib import admin
from .models import Articles, GameRecord

@admin.register(Articles)
class ArticlesAdmin(admin.ModelAdmin):
    # Что видим в списке вопросов
    list_display = ('id', 'question', 'answer', 'variant_1', 'variant_2')
    # По каким полям ищем
    search_fields = ('question', 'answer')
    # Фильтр справа (по правильным ответам, если нужно)
    list_filter = ('answer',)
    # Позволяет менять ответы прямо в списке, не заходя внутрь вопроса
    list_editable = ('answer',)
    # Пагинация (по 20 вопросов на страницу)
    list_per_page = 20

@admin.register(GameRecord)
class GameRecordAdmin(admin.ModelAdmin):
    # Формируем красивую таблицу рекордов
    list_display = ('player_name', 'score_display', 'date')
    # Фильтр по датам и количеству очков
    list_filter = ('date', 'correct_answers')
    # Поиск по имени игрока
    search_fields = ('player_name',)
    # Запрещаем редактировать рекорды (чтобы никто не подкрутил себе очки)
    readonly_fields = ('player_name', 'correct_answers', 'total_questions', 'date')

    # Кастомная колонка для отображения счета в виде "15 / 20"
    def score_display(self, obj):
        return f"{obj.correct_answers} / {obj.total_questions}"
    score_display.short_description = 'Результат'