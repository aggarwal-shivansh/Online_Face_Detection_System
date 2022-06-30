from django.contrib.auth import authenticate,login
from django.http import HttpResponse
from django.shortcuts import render, redirect
from datetime import datetime
from home.models import SignUp
from django.contrib import messages
import face_recognition
import cv2,os
import dlib
from deepface import DeepFace

#face detection view
#-------------------------
def facedect(loc):
    cam = cv2.VideoCapture(0)
    s, img = cam.read()
    # cv2.imshow('frame',img)

    if s:
        BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        MEDIA_ROOT = os.path.join(BASE_DIR, '')

        loc = (str(MEDIA_ROOT) + loc)
        print(loc)
        face_1_image = face_recognition.load_image_file(loc)
        face_1_face_encoding = face_recognition.face_encodings(face_1_image)[0]

        #
        # small_frame = cv2.resize(img, (0, 0), fx=0.25, fy=0.25)
        # rgb_small_frame = small_frame[:, :, ::-1]

        face_locations = face_recognition.face_locations(img)
        face_encodings = face_recognition.face_encodings(img, face_locations)

        check = face_recognition.compare_faces(face_1_face_encoding, face_encodings)
        print(check[0])
        var = cam.release
        if check[0]:
            return True
        else:
            return False
#-------------------------

# Create your views here.
def index(request):
    return render(request, 'index.html')

def signIn(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)

        if user is not None:
            obj1 = SignUp.objects.get(username=username)
            if facedect('home\profile_images\dp.png'):
                login(request, user)
                return render(request,'detect.html')
        else:
            messages.success(request, 'Bad Credentials')
            return render(request, 'signIn.html')
    return render(request, 'signIn.html')

def signUp(request):
    signup = SignUp()
    if request.method == "POST":
        signup.name = request.POST['name']
        signup.email = request.POST['email']
        signup.username = request.POST['username']
        signup.password = request.POST['password']
        signup.face_shot = request.POST['img']
        signup.date = datetime.today()
        # signup = SignUp(name=name, email=email, username=username, password=password, date = datetime.today())
        signup.save()
        messages.success(request, 'User Created Successfully')
        return redirect('signIn')
    return render(request,'signUp.html')

def contact(request):
    return render(request,'contact.html')

def detect(request):
    return render(request,'detect.html')

def features(request):
    # cam = cv2.VideoCapture(0)
    # s, img_curr = cam.read()

    models = ["VGG-Face", "Facenet", "Facenet512", "OpenFace", "DeepFace", "DeepID", "ArcFace", "Dlib", "SFace"]

    # face verification
    result = DeepFace.verify(img1_path='C:/Users/shiva/Pictures/Saved Pictures/dp.png', img2_path="C:/Users/shiva/Pictures/Saved Pictures/dp.png")

    # face recognition
    # df = DeepFace.find(img_path="C:/Users/shiva/Pictures/Saved Pictures/dp.png", db_path="C:/workspace/my_db", model_name=models[1])

    # facial attributes recognition
    obj = DeepFace.analyze(img_path="C:/Users/shiva/Pictures/Saved Pictures/dp.png", actions=['age', 'gender', 'race', 'emotion'])
    context = {
        "variable":obj
    }
    return render(request,'features.html',context)
