from django.db import models
from django.utils import timezone

# Create your models here.

class Articles(models.Model):
    question = models.TextField('Вопрос')
    variant_1 = models.CharField('Вариант ответа №1')
    variant_2 = models.CharField('Вариант ответа №2')
    variant_3 = models.CharField('Вариант ответа №3')
    variant_4 = models.CharField('Вариант ответа №4')
    answer = models.CharField('Правильный ответ')

    def __str__(self):
        return self.question
    
    class Meta:
        verbose_name = 'Вопрос для 1 раунда'
        verbose_name_plural = 'Вопросы для 1 раунда'

class GameRecord(models.Model):
    player_name = models.CharField(max_length=100, default="Киноман")
    correct_answers = models.IntegerField()
    total_questions = models.IntegerField()
    date = models.DateTimeField(auto_now_add=True) # Сама ставит дату создания

    class Meta:
        # Сортировка: сначала самые умные (рекорды), потом самые свежие
        ordering = ['-correct_answers', '-date'] 

    def __str__(self):
        return f"{self.player_name}: {self.correct_answers}/{self.total_questions}"