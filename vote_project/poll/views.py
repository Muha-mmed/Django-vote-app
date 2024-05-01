from django.shortcuts import render, redirect,  get_object_or_404
from django.contrib.auth import authenticate,login,logout
from .form import signupform,LoginForm
from django.contrib.auth.decorators import login_required
from .models import Poll
from django.contrib import messages


# Create your views here.
@login_required(login_url='login')
def index(request):
    all_poll = Poll.objects.all()
    return render(request,'index.html',{'polls': all_poll})


def createPoll(request):
    if request.method == 'POST':
        user = request.user
        question = Poll.objects.create(
            user=user,
            question=request.POST['question'],
            option1=request.POST['option1'],
            option2=request.POST['option2'],
            option3=request.POST['option3']
        )
        question.save()
        return redirect('index')
    return render(request,'createPoll.html')
        


def votePage(request, poll_id):
    poll = Poll.objects.get(pk=poll_id)
    user_voted_key = f'user_voted_{poll_id}'
    
    if request.method == 'POST':
        
        user_has_voted = request.session.get(user_voted_key,False)
        
        # Check if the selected_option is None or empty
        if 'option' not in request.POST:
            messages.error(request, "Please select an option.")
            return redirect('votePage', poll_id=poll_id)
        
        selectedOption = request.POST['option']
        
        if user_has_voted:
            messages.error(request, "you have already vote for this poll.")
            return redirect('votePage', poll_id=poll_id)
        # Update the vote count for the selected option
        if selectedOption == poll.option1:
            poll.option1_count += 1
        elif selectedOption == poll.option2:
            poll.option2_count += 1
        elif selectedOption == poll.option3:
            poll.option3_count += 1
        else:
           messages.error(request," Option must be select")
        poll.save()
        request.session[user_voted_key] = True
        # messages.success(request, "Your vote has been recorded.")
        return redirect('result', poll_id=poll.id)  # Redirect to the home page or any other appropriate page after voting
    
    return render(request, 'vote.html', {'poll': poll})


def result(request,poll_id):
    poll = get_object_or_404(Poll, pk= int(poll_id))
    return render(request, 'result.html', {'poll': poll})


def login_user(request):
    error_msg = None
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username,password= password)
            if user:
                login(request, user)
                return redirect('index')
            else:
                error_msg = 'Invalid Email address or password'
    else:
        form = LoginForm()
        error_msg = None
    return render(request,'login.html',{'form': form, 'error_msg': error_msg})


def register(request):
    if request.method == 'POST':
        form = signupform(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/login')
    else:
        form = signupform()        
    return render(request,'signup.html',{'form': form})


def delete_poll(request, poll_id):
    poll = Poll.objects.get(pk=poll_id)
    if request.user == poll.user:  # Check if the current user is the creator of the post
        poll.delete()
        messages.success(request, "Poll deleted successfully.")
    else:
        messages.error(request, "You are not authorized to delete this poll.")
    return redirect('index')


def logout_user(request):
    logout(request)
    return redirect('login')