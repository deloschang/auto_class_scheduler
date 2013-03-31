from django.shortcuts import render_to_response

def home(request):
    return render_to_response("main.html")

def loggedin(request):
    return render_to_response("logged-in.html")
    

