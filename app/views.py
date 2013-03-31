from django.shortcuts import render_to_response
from social_auth.models import UserSocialAuth

def home(request):
    return render_to_response("main.html")

def loggedin(request):
    tokens = UserSocialAuth.get_social_auth_for_user(request.user).get().tokens
    return render_to_response("logged-in.html", {'tokens': tokens})
    

