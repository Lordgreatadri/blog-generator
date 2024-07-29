from django.shortcuts import render, redirect
# from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User, auth
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from django.conf import settings
from .models import BlogPost
from pytube import YouTube   #pip3 install pytube to enable pytube usage
import assemblyai as aai
import yt_dlp
import openai 
import json
import os 




# Create your views here.
@login_required   #now creat LOGIN_URL in setting to make it accessible to Django
def index(request):
    return render(request, 'index.html')

@csrf_exempt  #this is necessary to exempt the CSRF token errors from the request body if not added from the frontend
def generate_blog(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            youtube_link = data['link']

            # return HttpResponse('Only POST request is allowed', status=200)
        except json.JSONDecodeError: #(KeyError, json.JSONDecodeError):
            print('Invalid: ', json.JSONDecodeError)
            return HttpResponse('Invalid JSON data sent', status=400)
        except Exception as e:
            print(f"This error: " +e.message)
            return HttpResponse(f'Error occured : ' +e, status=500)
        
        # get the title of the video using python library called Pytube API
        title = youtube_title(youtube_link)

        # get the transcript of the video 
        transcription = get_transcription(youtube_link)

        if not transcription:
            return HttpResponse({'error':'Failed to get transcription', 'status':400}, status=400)


        #generate the blog with OpenAI
        blog_content = generate_blog_from_transcript(transcription)
        if not blog_content:
            return HttpResponse({'error':'Failed to generate blog content', 'status':400}, status=400)

        
        # save article to the database
        blog_article = BlogPost.objects.create(
            user = request.user,
            youtube_title = title,
            youtube_url = youtube_link,
            generated_content = blog_content
        )
        blog_article.save()

        # return blog article  as a response
        return HttpResponse({'status':200, 'content':blog_content}, status=200)
    else:
        return HttpResponse({'message':'Only POST request is allowed'}, status=405)
    


    # getting the title
def youtube_title(ytitle):
    title = YouTube(ytitle)
    youtube_title = title.title
    return youtube_title


def download_audio(link):
    yt = YouTube(link)
    video = yt.streams.filter(only_audio=True).first()
    output = video.download(output_path = settings.MEDIA_ROOT)
    base, ext = os.path.splitext(output)
    audio_file = base + '.mp3'
    os.rename(output, audio_file)
    return audio_file


def get_transcription(link):
    audio_file = download_audio(link)
    aai.settings.api_key = os.getenv('ASSEMBLY_API_KEY')
    transcriber = aai.Transcriber()
    transcript = transcriber.transcribe(audio_file)
    return transcript.text


def generate_blog_from_transcript(transcript):
    # generate blog content based on the transcript
    openai.api_key = os.getenv('OPEN_AI_SECRET_KEY')

    prompt = f"Based on the following transcript from a youtube video, please write a thorough, comprehensive, and well stractured blog article based on the transcript, but kindly don't make it look like a youtube video but a propper blog article.\n\nThe transcript: {transcript}\n\nArticle:"
    
    response = openai.Completion.create(
        model = "text-davinci-003",
        engine="davinci",
        prompt=prompt,
        max_tokens=1000,
    )

    return response.choices[0].text.strip()


def blogs(request):
    articles = BlogPost.objects.filter(user = request.user)
    return render(request, 'all-blogs.html', {'articles': articles})

def blogs_post(request, pk):
    post = BlogPost.objects.filter(user = request.user, id = pk).first()
    return render(request, 'blog-posts.html', {'post': post})


def user_signup(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password_confirmation = request.POST['password_confirmation']
        
        if password == password_confirmation:
            try :
                if User.objects.filter(email = email).exists():
                    messages.info(request, 'Email already exists')
                    return redirect('signup')
                elif User.objects.filter(username = username).exists():
                    messages.info(request, 'Username already exists')
                    # error_message = 'Username already exists'
                    return redirect('signup')
                
                user = User.objects.create_user(username, email, password)
                user.save()
                login(request, user)

                messages.success(request, 'Registration successful. You can login now.')
                return redirect('/', user)
            except Exception as e:
                messages.info(request, 'Error occurred while registering user')
                return redirect('signup')
        
        messages.info(request, 'The passwords you entered does not match')
        # error_message = 'The passwords you entered does not match'
        return redirect('signup')
    return render(request, 'signup.html')

def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        
        user = auth.authenticate(username = username, password = password)
        #user = authenticate(username = username, password = password)# use only if you imported authentication, login, logout = from django.contrib.auth import authenticate, login, logout
        if user is not None:
            auth.login(request, user)
            # login(request, user) # use only if you imported authentication, login, logout = from django.contrib.auth import authenticate, login, logout
            messages.success(request, 'Login successful')
            return redirect('/', user)
        else:
            # error_message = 'Username or password is incorrect'
            messages.info(request, 'Username or password is incorrect')
            return redirect('login')
        
    return render(request, 'login.html')

def user_logout(request):
    #logout(request) all works since we imported logout directly
    auth.logout(request)
    messages.success(request, 'You have been logged out')
    return redirect('login')