from django.contrib import admin
from .models import User, Session, Guess, Wordlist, Statistics

# Register your models here.

admin.site.register(User)
admin.site.register(Session)
admin.site.register(Guess)
admin.site.register(Wordlist)
admin.site.register(Statistics)