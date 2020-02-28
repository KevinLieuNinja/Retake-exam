from django.shortcuts import render, redirect
from django.contrib import messages
from .models import *
import bcrypt


def index(request):
    return render( request, 'index.html')

def register(request):
    errors = User.objects.register(request.POST)
    if len (errors) > 0:
        for key, error in errors.items():
            messages.error(request, error)
        return redirect("/")
    else:
        PW_hash = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt()).decode()
        user = User.objects.create(
            email=request.POST['email'].lower(), 
            password= PW_hash, 
            first_name=request.POST['first_name'],
            last_name=request.POST['last_name']
        )
        # THE LOGGED IN USER IS IN THIS SESSION ID 
        request.session['user_id'] = user.id
        # messages.success(request, 'YAYYYY YOURE IN!')
        return redirect('/dash')

# LOGGING IN STUFF
def login(request):
    errors = User.objects.login(request.POST)
    if errors:
        for error in errors:
            messages.error(request, error)
        return redirect('/')

    else:
        user = User.objects.filter(email=request.POST['email'].lower())
        if len(user) < 1 :
            messages.error(request, 'No ones using this lame email.')
            return redirect("/")

        if bcrypt.checkpw(request.POST['password'].encode(), user[0].password.encode()):
            print(f"LOG - Session val 'user_id' = {user[0].id}")

            # THE LOGGED IN USER IS IN THIS SESSION ID 
            request.session['user_id'] = user[0].id
            return redirect('/dash')
        else:
            messages.error(request, 'Wrong password!')
            return redirect('/')


# LOGGING OUT STUFF
def logout(request):
    request.session.clear()
    messages.success(request, "Log out successful!")
    print(f"LOG - Log out successful, redirecting to home")  
    return redirect("/")

# THIS IS THE MAIN PAGE
def dash(request):
    user_id = request.session['user_id']
    user = User.objects.get(id=user_id)
    context = {
        'all_thought' : Thought.objects.all(),
        'user' : user
    }

    return render(request, 'Dash.html' , context)

def createThought(request):
    errors= Thought.objects.basic_validator(request.POST)

    if len(errors) > 0:
        for k, value in errors.items():
            messages.error(request, value)
        return redirect('/createThought')

    else:
        user= User.objects.get(id = request.session['user_id'])
        Thought.objects.create(thought_con = request.POST['thought_con'], user = user)
        return redirect('/dash')

# view this thought from a user
def viewThought(request, id):
    user_id = request.session['user_id']
    user = User.objects.get(id= user_id)

    context ={
        'user' : user,
        'thought' : Thought.objects.get(id=id)
    }

    return render(request, 'views.html', context)

def likedThought(request , id):
    user_id = request.session['user_id']
    user = User.objects.get(id= user_id)
    thought = Thought.objects.get(id=id)

    user.liked_thots.add(thought)
    thought.likes.add(user)

    return redirect('/viewThought/' + str(id))

def unlikeThought(request, id):
    user_id = request.session['user_id']
    user = User.objects.get(id = user_id)
    thought = Thought.objects.get(id=id)

    user.liked_thots.remove(thought)
    thought.likes.remove(user)

    return redirect('/viewThought/' + str(id))

def deleteThought(request, id):
    thought_com = Thought.objects.get(id = id)
    thought_com.delete() 
    return redirect('/dash')