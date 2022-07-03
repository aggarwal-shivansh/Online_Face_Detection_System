from django.contrib.auth import authenticate,login
from django.http import HttpResponse
from django.shortcuts import render, redirect
from datetime import datetime
from home.models import SignUp,Employee
from django.contrib import messages
from django.templatetags.static import static
#from django.conf.urls.static import static
import face_recognition
import cv2,os
from fpdf import FPDF
from deepface import DeepFace
from django.conf import settings
#face detection view
#-------------------------

#***************FACE-AUTHENTICATION-SYSTEM********************

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
            print("USER DETECTED AND AUTHENTICATED -> ")
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
        signup.face_shot = request.FILES['img']
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
    if request.method == "POST":
        image_path = request.POST['img1']
        print(image_path)
        image_path = "images/"+ str(image_path)
        image_source = "."+static(image_path)
        try:
            obj = DeepFace.analyze(img_path=image_source, actions=['age', 'gender', 'race', 'emotion'])
            est_age = obj['age']//10
            temp = est_age*10
            est_age = (est_age+1)*10
            context = {
                "face_detected": "true",
                "variable": obj,
                "age_start":temp,
                "age_end":est_age,
                "src":image_path,
                "flag":1,
                "face":1
            }
            return render(request, 'features.html',context)
        except:
            context = {
                "face_detected": "false",
                "note": 'NO FACE DETECTED. Please enter an image containing face'
            }
            return render(request, 'features.html', context)

    models = ["VGG-Face", "Facenet", "Facenet512", "OpenFace", "DeepFace", "DeepID", "ArcFace", "Dlib", "SFace"]

    # face verification
    # result = DeepFace.verify(img1_path='./static/dp.png', img2_path="C:/Users/shiva/Pictures/Saved Pictures/dp.png")

    # face recognition
    # df = DeepFace.find(img_path="C:/Users/shiva/Pictures/Saved Pictures/dp.png", db_path="C:/workspace/my_db", model_name=models[1])

    # facial attributes recognition
    return render(request, 'features.html',{"flag":0,"face":0})

def attendance(request):
    if request.method == "POST":
        #urlpatterns = static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
        obj = Employee.objects.all()
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=15)
        for name in obj:
            print(name.face_shot)
            if facedect("profile_images\profile_images\/"+str(name.face_shot)):
                print("employee marked present ->  "+ name.name)
                pdf.cell(200, 10, txt=str(name.enroll_id)+"   "+str(name.name)+"---> Present   "+str(datetime.now()), align='C')
                pdf.output("employees_present.pdf")
                break;
            else:
                print("user not present in database")

    return render(request, 'attendance.html')


def add_employee(request):
    add_emp = Employee()
    if request.method == "POST":
        add_emp.enroll_id = request.POST['enroll_id']
        add_emp.name = request.POST['name']
        add_emp.email = request.POST['email']
        add_emp.face_shot = request.FILES['img12']
        add_emp.date = datetime.today()
        add_emp.save()
        return redirect('attendance')
    return render(request, 'add_employee.html',{'flag':0})

