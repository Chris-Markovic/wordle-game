[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-22041afd0340ce965d47ae6ef1cefeee28c7c493a6346c4f15d667ab976d596c.svg)](https://classroom.github.com/a/JI7PxpoW)

# Wordle

A browser-based Wordle clone built with Django.
Guess the 5-letter word in 6 attempts. After each guess, letters are highlighted
green (correct position), orange (wrong position), or grey (not in word). You are able to view your game history 
and statistics. The admin can edit/manage all of the users and other data and tables.

## Features
- User registration and login
- Unlimited games
- Word validation with dictionary API - the app checks whether the guess is a real word
- Game history for each user
- Win/loss statistics and win streak tracking
- Admin panel for making admin changes

## Installation Instructions

1. Clone the repository and go into the folder
2. Create a virtual environment: python -m venv venv
3. Activate it: venv\Scripts\activate (on Windows) or source venv/bin/activate (on Mac)
4. Install packages: pip install -r requirements.txt
5. Run migrations: python manage.py migrate
6. Start the server: python manage.py runserver
7. Open the local server at: http://127.0.0.1:8000

## Test accounts
- Admin: username= admin, password= imc-admin
- User: username= user1, password= imc-user

## How to play

**Playing a game**: Log in to the pre-made accounts or register and click Play. Type a 5-letter word as your guess and submit.
Tiles turn green (right place), orange (wrong place), or grey (not in word).

**Game history**: Click History in the navbar to see all past games.

**Statistics**: Click Stats to see your win rate, total games, and current streak.

**How to return from History/Stats to home page**: When you enter the history or stats and want to go back to the game,
click the "Wordle" logo on the left of the navbar to return.

**Admin panel**: Log in as admin (admin/imc-admin) and go to /admin/ to manage
users, sessions, and statistics.

**Pre-loaded accounts**:
- Admin: username=admin, password=imc-admin
- User: username=user1, password=imc-user

## Running tests
pytest = all tests
pytest tests/test_game_logic.py = run a specific test

## Demo video link
https://youtu.be/A02uV8Gx_YY