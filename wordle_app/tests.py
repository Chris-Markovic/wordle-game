from django.test import TestCase
import pytest
from django.contrib.auth import get_user_model
from wordle_app.models import Session, Guess
# Create your tests here.



@pytest.mark.django_db
class TestCheckGuess:
    def setup_method(self): #Creates the user and establishes the session for the user
        User = get_user_model()
        user = User.objects.create_user('testuser','x','pass')
        self.session = Session.objects.create(user=user, target_word='CRANE')

    def test_all_correct(self): #Tests the case where all the letters are correct
        g = Guess(session=self.session, guessed_word='CRANE')
        assert g.check_guess('CRANE') == 'GGGGG'

    def test_no_match(self): #Tests the case where no letters are correct
        g = Guess(session=self.session, guessed_word='GHOST')
        assert g.check_guess('CRANE') == 'XXXXX'

    def test_orange(self): #Checks when the letters are inside the word but not in the right place
        g = Guess(session=self.session, guessed_word='READS')
        result = g.check_guess('CRANE')
        assert result[0] == 'O'
        assert result[1] == 'O'
        assert result[2] == 'G'
        assert result[3] == 'X'

    def test_duplicate_letters(self): #Tests when there are duplicate letters in the guess, needs to return only as many oranges or greens as there are in the target word
        g = Guess(session=self.session, guessed_word='EERIE')
        result = g.check_guess('BREED')



@pytest.mark.django_db
class TestStatistics:
    def setup_method(self): #Creates the user and establishes the session for the user
        User = get_user_model()
        user = User.objects.create_user('statuser','x','pass')
        from wordle_app.models import Statistics
        self.stats = Statistics.objects.create(user=user)

    def test_winrate_zero_games(self): #Test whether the winrate is 0% when no games have been played
        assert self.stats.calculate_winrate() == 0.0

    def test_winrate_calculation(self): #Tests the winrate calculation with actual wins and games
        self.stats.total_games = 10
        self.stats.games_won = 7
        assert self.stats.calculate_winrate() == 70.0

    def test_streak_increments_on_win(self): #Tests whether the streak counter increases when a game is won
        self.stats.update_stats(won=True)
        assert self.stats.current_streak == 1

    def test_streak_resets_on_loss(self): #Tests whether the streak ends and resets when a user loses
        self.stats.current_streak = 5
        self.stats.update_stats(won=False)
        assert self.stats.current_streak == 0


from unittest.mock import patch, MagicMock #Searched how to test the api calls withput actually using real calls because it would slow down the tests and found this library on this stie: https://opensource.com/article/21/9/unit-test-python
from wordle_app.api import DictionaryAPI

def test_check_word_exists_valid(): #Tests the api call when it sends the guessed word to the dictionary to find out if its a real word(in this case it is)
    api = DictionaryAPI()
    mock_resp = MagicMock()
    mock_resp.status_code = 200
    with patch('wordle_app.api.requests.get', return_value=mock_resp):
        assert api.check_word_exists('crane') == True

def test_check_word_exists_invalid(): #Tests the api call when it sends the guessed word to the dictionary to find out if its a real word(in this case it isnt)
    api = DictionaryAPI()
    mock_resp = MagicMock()
    mock_resp.status_code = 404
    with patch('wordle_app.api.requests.get', return_value=mock_resp):
        assert api.check_word_exists('zzzqq') == False



@pytest.mark.django_db
def test_start_new_game_creates_session(): #Checks if a session is created when a user starts a new game and if all of the api calls work correctly
    User = get_user_model()
    user = User.objects.create_user('gameuser','x','pass')
    with patch('wordle_app.game.DictionaryAPI') as MockAPI:
        instance = MockAPI.return_value
        instance.get_target_word.return_value = 'CRANE'
        instance.get_word_definition.return_value = 'A large bird'
        instance.check_word_exists.return_value = True
        from wordle_app.game import WordleApp
        app = WordleApp(user)
        session = app.start_new_game()
        assert session.target_word == 'CRANE'
        assert session.user == user


@pytest.mark.django_db
def test_invalid_guess_rejected(client): #Tests that the word is returned as an invalid word when posted with the check_word_exists() and is actually invalid- "ZZZZZ"
    User = get_user_model()
    user = User.objects.create_user('viewuser','x','pass')
    client.login(username='viewuser', password='pass')
    session = Session.objects.create(user=user, target_word='CRANE')
    with patch('wordle_app.views.DictionaryAPI') as MockAPI:
        MockAPI.return_value.check_word_exists.return_value = False
        resp = client.post('/guess/', {'guess': 'ZZZZZ'})
    assert b'not a valid word' in resp.content




@pytest.mark.django_db
def test_register_creates_user(client): #Registers a new user and tests whether this user actually exists after being created
    resp = client.post('/register/', {'username':'newuser', 'password1':'Str0ngPass!', 'password2':'Str0ngPass!'})
    assert resp.status_code == 302
    User = get_user_model()
    assert User.objects.filter(username='newuser').exists()

def test_home_requires_login(client): #Tets the rule that the home screen should require you to log in first and that it redirects you to the login page
    resp = client.get('/')
    assert resp.status_code == 302
    assert '/login/' in resp['Location']