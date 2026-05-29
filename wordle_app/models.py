from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.

class User(AbstractUser):
    is_admin = models.BooleanField(default=False)

    def get_game_history(self):
        return self.sessions.order_by('-start_time')

    def admin_delete_user(self, user_id):
        User.objects.filter(id=user_id).delete()

    def admin_reset_user_stats(self, user_id):
        stats = Statistics.objects.get(user_id=user_id)
        stats.total_games = 0
        stats.games_won = 0
        stats.current_streak = 0
        stats.save()

class Session(models.Model):
    user = models.ForeignKey('User', on_delete=models.CASCADE, related_name='sessions')
    target_word = models.CharField(max_length=5)
    word_definition = models.TextField(blank=True)
    start_time = models.DateTimeField(auto_now_add=True)
    end_time = models.DateTimeField(null=True, blank=True)
    game_won = models.BooleanField(null=True)


    def mark_finished(self, won):
        from django.utils import timezone
        self.game_won = won
        self.end_time = timezone.now()
        self.save()

    def get_duration_minutes(self):
        if self.end_time:
            return (self.end_time - self.start_time).seconds // 60
        return None



class Guess(models.Model):
    session = models.ForeignKey('Session', on_delete=models.CASCADE, related_name='guesses')
    guessed_word = models.CharField(max_length=5)
    result_colors = models.CharField(max_length=5)
    time_stamp = models.DateTimeField(auto_now_add=True)

    def check_guess(self, target_word):
        result = [None, None, None, None, None]
        target = list(target_word.upper())
        guess = list(self.guessed_word.upper())

        for i in range(5):
            if guess[i] == target[i]:
                result[i] = 'G'
                target[i] = None

        for i in range(5):
            if result[i] is None:
                if guess[i] in target:
                    result[i] = 'O'
                    target[target.index(guess[i])] = None
                else:
                    result[i] = 'X'

        self.result_colors = ''.join(result)
        self.save()
        return self.result_colors

    def get_letter_color_pairs(self):
        return list(zip(self.guessed_word, self.result_colors))




class Wordlist(models.Model):
    word_id = models.AutoField(primary_key=True)
    target_word = models.CharField(max_length=5, unique=True)
    word_definition = models.TextField(blank=True)
    date_discovered = models.DateTimeField(auto_now_add=True)



class Statistics(models.Model):
    user = models.OneToOneField('User', on_delete=models.CASCADE, related_name='statistics')
    total_games = models.IntegerField(default=0)
    games_won = models.IntegerField(default=0)
    current_streak = models.IntegerField(default=0)


    def update_stats(self, won):
        self.total_games += 1
        if won:
            self.games_won += 1
            self.current_streak += 1
        else:
            self.current_streak = 0

        self.save()

    def calculate_winrate(self):
        if self.total_games == 0:
            return 0
        else:
            return (self.games_won / self.total_games) * 100