from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from .api import DictionaryAPI
from .models import Statistics
from django.contrib.auth.decorators import login_required
from .game import WordleApp
from .models import Session
from .models import Guess
# Create your views here.

class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = get_user_model()
        fields = ('username', 'password1', 'password2')

def register(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            Statistics.objects.create(user=user)
            return redirect("login")
    else:
        form = CustomUserCreationForm()
    return render(request, "wordle_app/register.html", {"form": form})

@login_required
def home(request):
    session = Session.objects.filter(user=request.user, game_won__isnull=True).first()
    if not session:
        app = WordleApp(request.user)
        session = app.start_new_game()
    guesses = session.guesses.all()
    remaining = 6 - guesses.count()
    return render(request, "wordle_app/game.html", {"session": session, "guesses": guesses, "guess_count": guesses.count(),'remaining_rows': range(remaining)})


@login_required
def submit_guess(request):
    if request.method != "POST":
        return redirect("home")
    word = request.POST.get("guess", "").upper().strip()
    session = Session.objects.filter(user=request.user, game_won__isnull=True).first()
    api = DictionaryAPI()

    if len(word) != 5 or not word.isalpha():
        guesses = session.guesses.all()
        return render(request, 'wordle_app/game.html', {'error': 'Please enter a 5-letter word.','session': session,'guesses': guesses,'guess_count': guesses.count(),'remaining_rows': range(6 - guesses.count()),})

    if not api.check_word_exists(word):
        guesses = session.guesses.all()
        return render(request, 'wordle_app/game.html', {'error': f'"{word}" is not a valid word.','session': session,'guesses': guesses,'guess_count': guesses.count(),'remaining_rows': range(6 - guesses.count()),})

    guess = Guess(session=session, guessed_word=word)
    colors = guess.check_guess(session.target_word)

    won = colors == 'GGGGG'
    if won or session.guesses.count() >= 6:
        session.mark_finished(won)
        session.user.statistics.update_stats(won)
        return redirect('game_over', session_id=session.id)

    return redirect('home')


@login_required
def game_over(request, session_id):
    session = Session.objects.get(id=session_id, user=request.user)
    return render(request, 'wordle_app/game_over.html', {'session': session,'guesses': session.guesses.all(),'won': session.game_won,})


@login_required
def history(request):
    sessions = request.user.get_game_history().filter(game_won__isnull=False)
    return render(request, 'wordle_app/history.html', {'sessions': sessions})

@login_required
def stats_view(request):
    stats, _ = Statistics.objects.get_or_create(user=request.user)
    return render(request, 'wordle_app/statistics.html', {'stats': stats,'winrate': stats.calculate_winrate(),
    })

