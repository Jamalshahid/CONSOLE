from fileinput import filename
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from dateutil.relativedelta import relativedelta
from datetime import timedelta, date
import datetime
from calendar import monthrange
import random
import threading
# from .detect import detect as yolo_model_detect
from PIL import Image
from io import BytesIO
import string

import matplotlib.pyplot as plt
# from tensorflow.keras.models import load_model
from django.conf import settings
import serial
import time
import base64
import cv2
import numpy as np
from fyp_project.defect_algos.cap_seated_lg import cap_seated_lg
from quality_assurance_system.models import *
from .defect_algos.cap_seated_lg import cap_seated_lg
from .defect_algos.cap_seated_md import cap_seated_md
from .defect_algos.cap_sealed_lg import cap_sealed_lg
from .defect_algos.cap_sealed_md import cap_sealed_md
from .defect_algos.cap_cocked_lg import cap_cocked_lg
from .defect_algos.cap_cocked_md import cap_cocked_md
from .defect_algos.product_on_bottle_lg import product_on_bottle_lg
from .defect_algos.product_on_bottle_md import product_on_bottle_md
from django.http import HttpResponse
from django.views.generic import View
from .utils import generateEtamuReport 
import mimetypes
import os
import pandas as pd
from django.core.mail import EmailMessage
import sqlite3
# from django.conf import settings
from ultralytics import YOLO

from django.http import FileResponse, Http404

# model1 = load_model('./mobilenetV2_original_dent.h5')
# model2 = load_model('./mobilenetV2_original_pob.h5')
# model3 = load_model('./mobilenetV2_original_scuff.h5')

main_model = YOLO('yolov8_model.pt')

            

def pdf_view(path):
    return FileResponse(open(path, 'rb'), content_type='application/pdf')


def generateEtamuReportView(request):

    generateEtamuReport()

    # Define Django project base directory
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    # Define text file name
    filename = 'report.pdf'
    # Define the full file path
    filepath = BASE_DIR + '/' + filename
    # Open the file for reading content
    path = open(filepath, 'r')
    # Set the mime type
    mime_type, _ = mimetypes.guess_type(filepath)
    # Set the return value of the HttpResponse
    response = HttpResponse(path, content_type=mime_type)
    # Set the HTTP header for sending to browser
    response['Content-Disposition'] = "attachment; filename=%s" % filename
    # Return the response value
    return response

    # return HttpResponse(pdf, content_type='application/pdf')


def emailEtamuReportView(request):

    # start_date = request.GET.get('start_date')
    # end_date = request.GET.get('end_date')

    generateEtamuReport()

    # Define Django project base directory
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    # Define text file name
    filename = 'report.pdf'
    # Define the full file path
    filepath = BASE_DIR + '/' + filename
    # Open the file for reading content
    path = open(filepath, 'r')

    subject = "E-Tamu Report"
    message = "PDF Attached Below"
    emails = ["aliabbaspanjwani7@gmail.com", request.GET.get('email')]
    mail = EmailMessage(subject, message, settings.EMAIL_HOST_USER, emails)
    # mail.attach('Report.pdf', pdf_view(filepath), 'application/pdf')
    mail.attach_file(filepath)
    
    try:
        mail.send(fail_silently = False)
        # return HttpResponse("Mail Sent")
        messages.success(request, 'Report emailed successfully.')
    except:
        # return HttpResponse("Mail Not Sent")
        messages.success(request, 'An error occured while emailing the report.')

    return redirect('home')


def rotate_motor(request):
    
    direction = request.POST.get('direction')
    ser = serial.Serial( port="COM3",    
             baudrate=9600, 
             bytesize=8, 
             timeout=1,
             stopbits=serial.STOPBITS_ONE )

    time.sleep(2)

    if direction == "right":
        ser.write("P|0400".encode('Ascii'))
    else:
        ser.write("P|-0400".encode('Ascii'))

    ser.close() 

    return JsonResponse({"rotate_45" : "done"}, status=200)

def align_camera(request):
    direction = request.POST.get('direction')
    bottle_size = request.POST.get('bottle_size')

    ser = serial.Serial( port="COM3", 
            baudrate=9600, 
            bytesize=8, 
            timeout=1,
            stopbits=serial.STOPBITS_ONE )

    time.sleep(2)
    
    large_bottle_distance = 3740 # Set how much distance to move the large-bottle
    medium_bottle_distance = 2000 # Set how much distance to move the medium-bottle
    
    if bottle_size == "Large":
        if direction=='up':
            ser.write(f"C|-{large_bottle_distance}".encode('Ascii')) 
        else:
            ser.write(f"C|{large_bottle_distance}".encode('Ascii'))
            
            
    elif bottle_size == "Medium":
        if direction=='up':
            ser.write(f"C|-{medium_bottle_distance}".encode('Ascii'))
        else:
            ser.write(f"C|{medium_bottle_distance}".encode('Ascii'))

    # if bottle_size == "md" and request.session.get('cam_pos', None) is None:
    #     ser.write("C|-3740".encode('Ascii'))
    # elif bottle_size == "lg" and request.session.get('cam_pos', None) is None:
    #     ser.write("C|-4080".encode('Ascii'))
    # elif bottle_size == "md" and request.session.get('cam_pos', None) == "lg":
    #     ser.write("C|340".encode('Ascii'))
    # elif bottle_size == "lg" and request.session.get('cam_pos', None) == "md":
    #     ser.write("C|-340".encode('Ascii'))


    # request.session["cam_pos"] = bottle_size


    ser.close()

    return JsonResponse({"camer_align" : "done"}, status=200)

def redirect_to_home(request):
    return redirect('home')

@login_required(login_url='login')
def team(request):
    urlObject = request.get_host() + request.path
    return render(request, "pages/team.html", {'showURL': urlObject})

@login_required(login_url='login')
def faqs(request):
    conn = sqlite3.connect("console_database.sqlite3")  
    cursor = conn.cursor()
    batch_data = cursor.execute("""
         SELECT batch_id, bottles_size,
         CASE WHEN status = "Unacceptable" THEN "False"
         ELSE "True"
         END, 
         status, case strftime('%m', datetime(date_of_inspection, 'unixepoch', 'localtime')) when '01' then 'Jan' when '02' then 'Feb' when '03' then 'March' when '04' then 'April' when '05' then 'May' when '06' then 'June' when '07' then 'July' when '08' then 'Aug' when '09' then 'Sept' when '10' then 'Oct' when '11' then 'Nov' when '12' then 'Dec' else '' end
         || strftime(' %d, %Y, %H:%M:%S', datetime(date_of_inspection, 'unixepoch', 'localtime'))
         FROM batches
         """)
    batch_data = list(map(lambda x: list(x), batch_data))
    conn.close()
    print(batch_data)
    params = {"batch_data": batch_data}
    
    urlObject = request.get_host() + request.path
    return render(request, "pages/faqs.html", {'showURL': urlObject, 'params': params})

@login_required(login_url='login')
def about(request):
    urlObject = request.get_host() + request.path
    return render(request, "pages/about.html", {'showURL': urlObject})

@login_required(login_url='login')
def index(request):
    
    conn = sqlite3.connect("console_database.sqlite3")  
    cursor = conn.cursor()
   # Line chart for current year
    # line_chart_result = cursor.execute("""
    #             select COUNT(CASE WHEN status="Acceptable" THEN 1 END), COUNT(CASE WHEN status="Marginal" THEN 1 END), 
    #             COUNT(CASE WHEN status="Unacceptable" THEN 1 END), strftime("%m",  datetime(date_of_inspection, 'unixepoch')) as 'month-year' 
    #             from bottles_inspection_result WHERE strftime("%Y", datetime(date_of_inspection, 'unixepoch'))=strftime("%Y", datetime('now'))  group by strftime("%m",  datetime(date_of_inspection, 'unixepoch'));
    #             """)
    line_chart_result = cursor.execute("""
                select COUNT(CASE WHEN status="Acceptable" THEN 1 END), COUNT(CASE WHEN status="Marginal" THEN 1 END), 
                COUNT(CASE WHEN status="Unacceptable" THEN 1 END), strftime("%Y-%m-%d",  datetime(date_of_inspection, 'unixepoch')) as 'month-year' 
                from bottles_inspection_result WHERE strftime("%Y-%m-%d", datetime(date_of_inspection, 'unixepoch')) BETWEEN strftime("%Y-%m-%d", date('now','localtime','-29 days')) AND 
                strftime("%Y-%m-%d", date('now','localtime'))  group by strftime("%d",  datetime(date_of_inspection, 'unixepoch'));
                """)
    today = date.today()
    Dateslist = [str(today - timedelta(days = day)) for day in range(29)]
    line_chart_result = line_chart_result.fetchall()
    line_chart_result_accept = []
    line_chart_result_margin = []
    line_chart_result_unaccept = []
    count = 0
    for i in range(len(Dateslist)):

        for j in line_chart_result:
            if j[-1] == Dateslist[i]:
                line_chart_result_accept.append(j[0])
                line_chart_result_unaccept.append(j[2])
                line_chart_result_margin.append(j[1])
                count += 1
                break
        Dateslist[i] = "/".join(Dateslist[i].split("-")[-1:0:-1])
        if count > 0:
            count = 0
            continue
        line_chart_result_accept.append(0)
        line_chart_result_unaccept.append(0)
        line_chart_result_margin.append(0)

        


    # Fetching the percentages of the status / Pie Chart
    pie_chart_result = cursor.execute("""
                    select ROUND((COUNT(CASE WHEN status="Acceptable" THEN 1 END)* 100/COUNT(*)), 2), ROUND((COUNT(CASE WHEN status="Marginal" THEN 1 END) * 100/COUNT(*)) , 2), 
                    ROUND((COUNT(CASE WHEN status="Unacceptable" THEN 1 END)* 100/COUNT(*)) , 2)
                    from bottles_inspection_result WHERE strftime("%Y-%m-%d", datetime(date_of_inspection, 'unixepoch')) BETWEEN strftime("%Y-%m-%d", date('now','localtime','-29 days')) AND 
                    strftime("%Y-%m-%d", date('now','localtime'));
                """)
    pie_chart_result = list(pie_chart_result.fetchone()) #(% of acceptable, % of marginal, % of unacceptable)
    
    
    # Fetching the individual counts of defect status/type in the current month

    # For Acceptable
    acceptable_count_bottles = cursor.execute("""SELECT Count(*) FROM bottles_inspection_result WHERE status='Acceptable' AND strftime("%Y-%m-%d", datetime(date_of_inspection, 'unixepoch')) BETWEEN strftime("%Y-%m-%d", date('now','localtime','-29 days')) AND 
                strftime("%Y-%m-%d", date('now','localtime'));""")
    acceptable_count_bottles = list(acceptable_count_bottles.fetchone())
    # For Marginal
    marginal_count_bottles = cursor.execute("""SELECT Count(*) FROM bottles_inspection_result WHERE status='Marginal' AND strftime("%Y-%m-%d", datetime(date_of_inspection, 'unixepoch')) BETWEEN strftime("%Y-%m-%d", date('now','localtime','-29 days')) AND 
                strftime("%Y-%m-%d", date('now','localtime'));""")
    marginal_count_bottles = list(marginal_count_bottles.fetchone())
    # For Unacceptable
    unacceptable_count_bottles = cursor.execute("""SELECT Count(*) FROM bottles_inspection_result WHERE status='Unacceptable' AND strftime("%Y-%m-%d", datetime(date_of_inspection, 'unixepoch')) BETWEEN strftime("%Y-%m-%d", date('now','localtime','-29 days')) AND 
                strftime("%Y-%m-%d", date('now','localtime'));""")
    unacceptable_count_bottles = list(unacceptable_count_bottles.fetchone())
    # For total bottles
    total_count_bottles = cursor.execute("""SELECT Count(*) FROM bottles_inspection_result WHERE strftime("%Y-%m-%d", datetime(date_of_inspection, 'unixepoch')) BETWEEN strftime("%Y-%m-%d", date('now','localtime','-29 days')) AND 
                strftime("%Y-%m-%d", date('now','localtime'));""")
    total_count_bottles = list(total_count_bottles.fetchone())
    
    conn.close()
    
    urlObject = request.get_host() + request.path
    # count_of_total_bottles = Bottle.objects.count()
    # count_of_acceptable_bottles = Bottle.objects.filter(result="Acceptable").count()
    # count_of_unacceptable_bottles = Bottle.objects.filter(result="Unacceptable").count()

    # last_6_months_numbers = [(datetime.today().month - i - 1) % 12 + 1 for i in range(6)]
    # last_6_months_data = {}
    # # last_6_months_numbers.reverse()
    # month_names = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
    # current_month = datetime.today().month
    # current_year = datetime.today().year
    # print("************* dates *****************")
    # for i in range(-1,5):
    #     start_date = datetime(current_year,current_month,1)+relativedelta(months=-(i+1))
    #     end_date = datetime(current_year,current_month,1)+relativedelta(months=-i) 
    #     # end_date = str(end_date)
    #     # end_date = end_date.split(" ")[0]
    #     # end_date = end_date.split("-")
    #     # end_date = end_date[0]+"-"+end_date[1]+"-"
    #     last_6_months_data[month_names[last_6_months_numbers[i+1]-1]] = {"acceptable":Bottle.objects.filter(result="Acceptable", created_at__date__range=(start_date, end_date)).count(), "unacceptable":Bottle.objects.filter(result="Unacceptable", created_at__date__range=(start_date, end_date)).count()}

    #     print("from = {}, end = {}, total = {}".format(start_date, end_date, Bottle.objects.filter(created_at__date__range=(start_date, end_date)).count()))

    # print("*********** here is data **************")
    # print(last_6_months_data)


    # params = {
    #     "count_of_total_bottles": count_of_total_bottles, 
    #     "count_of_acceptable_bottles": count_of_acceptable_bottles, "count_of_unacceptable_bottles": count_of_unacceptable_bottles,
    #     "percentage_of_unacceptable_bottles": (count_of_unacceptable_bottles/count_of_total_bottles)*100,
    #     "percentage_of_acceptable_bottles": (count_of_acceptable_bottles/count_of_total_bottles)*100,
    #     "last_6_months_data": last_6_months_data
    #     }
    if acceptable_count_bottles[0] == 0:
        acceptable_count_bottles[0] = 1
    if unacceptable_count_bottles[0] == 0:
        unacceptable_count_bottles[0] = 1
    if marginal_count_bottles[0] == 0:
        marginal_count_bottles[0] = 1
    if total_count_bottles[0] == 0:
        total_count_bottles[0] = 1
        
    params = {"line_chart_accept_results": line_chart_result_accept, "line_chart_unaccept_results": line_chart_result_unaccept, 
              "line_chart_marginal_results": line_chart_result_margin, "pie_chart_results": pie_chart_result,
              "acceptable_count_bottles": acceptable_count_bottles[0], "unacceptable_count_bottles": unacceptable_count_bottles[0],
              "marginal_count_bottles": marginal_count_bottles[0], "total_count_bottles": total_count_bottles[0], "date_range_chart": Dateslist,
              "percent_acceptable": int((acceptable_count_bottles[0]/total_count_bottles[0])*100), "percent_unacceptable": int((unacceptable_count_bottles[0]/total_count_bottles[0])*100),
              "percent_marginal": int((marginal_count_bottles[0]/total_count_bottles[0])*100),
              }
    
    

    return render(request, "pages/home.html", {'showURL': urlObject, "params": params})


@login_required(login_url='login')
def quality_check_page(request):
    urlObject = request.get_host() + request.path
    return render(request, "pages/quality_check.html", {'showURL': urlObject})


@login_required(login_url='login')
def results_page(request):
    urlObject = request.get_host() + request.path
    conn = sqlite3.connect("console_database.sqlite3")  
    cursor = conn.cursor()
    dat = []
    data = cursor.execute(f"""
        SELECT strftime('%Y-%m-01 00:00:00', datetime(date_of_inspection, 'unixepoch'))||' GMT+0500', SUM(total_bottles) FROM batches WHERE status='Acceptable' AND strftime('%Y-%m-%d',  datetime(date_of_inspection, 'unixepoch')) >= date('now','-1 year') AND 
        strftime('%Y-%m-%d', datetime(date_of_inspection, 'unixepoch'))<=date('now') GROUP BY strftime('%Y-%m', datetime(date_of_inspection, 'unixepoch'))
        """)
    
    data = data.fetchall()
    for i in data:
        dat.append({"x": i[0], "y":i[1]})
    print(data)
    conn.close()
    
    return render(request, "pages/results.html", {'showURL': urlObject, "data_lst": dat})
    
def get_bottle_details(request):
    bottle_id = request.POST.get('bottle_id')
    bottle = Bottle.objects.filter(id=bottle_id)[0]
    params = getAllEntriesForBottle(bottle)
    print(params)
    return render(request, "pages/result_modal_body.html", params)


def loginPage(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')
            print(username, password)
            user = authenticate(request, username=username, password=password)
            print(user)
            if user is not None:
                login(request, user)
                messages.success(request, 'Login successfull.')
                return redirect('home')
            else:
                messages.error(request, 'Username OR password is incorrect')

        return render(request, 'auth/login.html')


def saveBottleDefectEntry(defects):

    final_result = evaluate_final_result(defects)

    bottle = Bottle(result=final_result)
    bottle.save()

    for defect in defects:
        bottle_defect = BottleDefect(bottle=bottle, defect_name=defect["defect_name"], result=defect["defect_result"])
        bottle_defect.save()

    return bottle


def inspect(request):
    defects = []
    defects = cap_seated_defect_check(request.POST.get('bottle_size'), defects)
    if(defects[0]["defect_result"] != "Unacceptable"):
        defects = cap_cocked_defect_check(request.POST.get('bottle_size'), defects)
    else:
        defects.append({"defect_name" : str(len(defects)+1)+". Cap Cocked", "defect_result" : "Acceptable"})
    
    defects = cap_sealed_defect_check(request.POST.get('bottle_size'), defects)
    defects = product_on_bottle_check(request.POST.get('bottle_size'), defects)


    print("*********** final result +++++++++++++")
    print(defects)

    params = getAllEntriesForBottle(saveBottleDefectEntry(defects))

    return render(request, "pages/result_modal_body.html", params)


def evaluate_final_result(defects):
    acceptable = True
    for defect in defects:
        if defect["defect_result"] != "Acceptable":
            acceptable = False
    
    if acceptable:
        return "Acceptable"
    else:
        return "Unacceptable"


def cap_seated_defect_check(bottle_size, defects):
    # front_image = "./defect_algos/inp_img_1.jpg"
    front_image = "./output.jpg"
    # front_image = "fyp_project/defect_algos/inp_img_1.jpg"
    if(bottle_size == "md"):
        cap_seated = cap_seated_md(front_image)
    else:
        cap_seated = cap_seated_lg(front_image)

    defects.append({"defect_name" : str(len(defects)+1)+". Cap Not Seated", "defect_result" : cap_seated})

    return defects



def product_on_bottle_check(bottle_size, defects):
    front_image = "./output.jpg"
    # front_image = "./defect_algos/inp_img_1.jpg"
    # front_image = "fyp_project/defect_algos/inp_img_1.jpg"
    if(bottle_size == "md"):
        product_on_bottle = product_on_bottle_md(front_image)
    else:
        product_on_bottle = product_on_bottle_lg(front_image)

    defects.append({"defect_name" : str(len(defects)+1)+". Product On Bottle", "defect_result" : product_on_bottle})

    return defects



def cap_sealed_defect_check(bottle_size, defects):
    front_image = "./output.jpg"
    # front_image = "./defect_algos/inp_img_1.jpg"
    # front_image = "fyp_project/defect_algos/inp_img_1.jpg"
    if(bottle_size == "md"):
        cap_sealed = cap_sealed_md(front_image)
    else:
        cap_sealed = cap_sealed_lg(front_image)

    defects.append({"defect_name" : str(len(defects)+1)+". Cap Not Sealed", "defect_result" : cap_sealed})

    return defects



def cap_cocked_defect_check(bottle_size, defects):
    front_image = "./output.jpg"
    # front_image = "./defect_algos/inp_img_1.jpg"
    # front_image = "fyp_project/defect_algos/inp_img_1.jpg"
    if(bottle_size == "md"):
        cap_cocked = cap_cocked_md(front_image)
    else:
        cap_cocked = cap_cocked_lg(front_image)

    defects.append({"defect_name" : str(len(defects)+1)+". Cap Cocked", "defect_result" : cap_cocked})

    return defects


def logoutUser(request):
    logout(request)
    messages.success(request, 'logout successfull.')
    return redirect('login')


def getAllEntriesForBottle(bottle_obj):
    bottle_defects = BottleDefect.objects.filter(bottle_id = bottle_obj)

    entries = []
    for bottle_defect in bottle_defects:
        temp = {}
        temp["defect_name"] = bottle_defect.defect_name
        temp["defect_result"] = bottle_defect.result
        
        entries.append(temp)

    params = {"result" : bottle_obj.result, "entries" : entries}

    return params


def save_img_on_server(request):
    i = request.POST.get('i')

    base64_img = request.POST.get('img_dataUrl')
    encoded_data = base64_img.split(',')[1]

    nparr = np.fromstring(base64.b64decode(encoded_data), np.uint8)
    target_img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    my_pic_path = "fyp_project/defect_algos/inp_img_" + str(i) + ".jpg"
    img_saved = cv2.imwrite(my_pic_path, target_img)
    print("image saved {} ".format(img_saved))

    return JsonResponse({"result" : "image saved {} ".format(img_saved)}, status=200)


# def img_model_inspect(request):
    
    
#     offset = request.POST.get('img').index(',') + 1
#     img_bytes = base64.b64decode(request.POST.get('img')[offset:])
#     img = Image.open(BytesIO(img_bytes))
    
#     # img = img.resize((224, 224), Resampling.HAMMING)
#     # img = img.convert('RGB')
#     img  = np.array(img)
#     img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
#     # img = cv2.resize(img, (224, 224))
#     # img = cv2.cvtColor(img, cv2.COLOR_RGBA2RGB)

#     # img = img.astype(np.float32)
#     # img = cv2.cvtColor(img, cv2.COLOR_GRAY2RGB)
#     # img = image_extract(img)
    
#     img = cv2.resize(img, (224, 224), interpolation=cv2.INTER_CUBIC)
    
#     img = np.array(list(reversed(img)))
#     # img= img[0:2880,937:2497]
#     cv2.imwrite("output.jpg", img=img)
    
#     # img = cv2.cvtColor(img, cv2.COLOR_RGBA2RGB)
#     # img = img.astype("float32")
#     # image = plt.imshow(img)
#     # plt.plot()
#     # plt.show()
#     # print("start")
#     # np_img = np.array(myfile)
#     # img = cv2.resize(q, (224, 224))
#     # print(os.listdir("../"))
    
#     model1 = load_model('./mobilenetV2_original_dent.h5')
#     model2 = load_model('./mobilenetV2_original_pob.h5')
#     model3 = load_model('./mobilenetV2_original_scuff.h5')
#     # model3 = load_model('./mobilenetV2_original.h5')
#     img = img / 255.0
#     # img = cv2.resize(img, dsize=(224, 224), interpolation=cv2.INTER_CUBIC)
#     img = img.reshape(1,224,224, 3)
    
    
#     label1 = model1.predict(img)
#     label2 = model2.predict(img)
#     label3 = model3.predict(img)
#     # label3 = model3.predict(img)
#     p1=np.argmax(label1)
#     p2=np.argmax(label2)
#     p3 = np.argmax(label3)
#     # p3=np.argmax(label3)

#     # paras = {0: "acceptable", 1: "marginal", 2: "unacceptable"}
#     # par = {0:"cap", 1: "bottle", 2:"dent"}
#     # print(p)
#     # params = {"defect_name": par[p], "defect_result": paras[p]}

#     # return render(request, "pages/result_modal_body.html", params)
#     # para = {"d1": p1, "d2":p2, "d3":p3}
#     para = {"d1": str(p1), "d2": str(p2), "d3":str(p3)}
#     return JsonResponse(para)

# def model_inspect(img):
#     global model1, model2, model3
#     label1 = model1.predict(img)    #dent
#     label2 = model2.predict(img)    #pob
#     label3 = model3.predict(img)    #scuff
    
#     p1=np.argmax(label1)
#     p2=np.argmax(label2)
#     p3 = np.argmax(label3)
    
#     paras = {0: "Acceptable", 1: "Marginal", 2: "Unacceptable"}
    
#     results = {"dent": paras[p1], "pob": paras[p2], "scuff": paras[p3]}
#     status = ""
#     if all(i=="Acceptable" for i in results.values()):
#         status = "Acceptable"
#     elif all(i!="Unacceptable" for i in results.values()):
#         status = "Marginal"
#     else:
#         status = "Unacceptable"
#     return [results, status]

def img_model_inspect(request):
    global main_model
    offset = request.POST.get('img').index(',') + 1
    img_bytes = base64.b64decode(request.POST.get('img')[offset:])
    img = Image.open(BytesIO(img_bytes))
    img  = np.array(img)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    
    # img = cv2.resize(img, (224, 224))
    # img = cv2.cvtColor(img, cv2.COLOR_RGBA2RGB)

    # img = img.astype(np.float32)
    # img = cv2.cvtColor(img, cv2.COLOR_GRAY2RGB)
    # img = image_extract(img)
    
    
    img= img[0:2880, 937:2497]
    img = np.array(list(reversed(img)))
    
    # img = image_resize(img, width=224, height=224)
    cv2.imwrite("output.jpg", img=img)
    # image = plt.imshow(img)
    # plt.plot()
    
    # img = img / 255.0
    # img = cv2.resize(img, dsize=(224, 224), interpolation=cv2.INTER_CUBIC)
    # img = img.reshape(1,224,224, 3)
    
    #Dont Disturb me please
    # defects = []
    # defects = cap_seated_defect_check(request.POST.get('bottle_size'), defects)
    # if(defects[0]["defect_result"] != "Unacceptable"):
    #     defects = cap_cocked_defect_check(request.POST.get('bottle_size'), defects)
    # else:
    #     defects.append({"defect_name" : str(len(defects)+1)+". Cap Cocked", "defect_result" : "Acceptable"})
    
    # defects = cap_sealed_defect_check(request.POST.get('bottle_size'), defects)
    # defects = product_on_bottle_check(request.POST.get('bottle_size'), defects)
    # print(defects)


    sob_defect= ""
    pob_defect=""
    dob_defect= ""
    cap_defect="Acceptable"
    status=""
    result = {"dent": "", "pob": "", "scuff": ""}
    
    results = main_model.predict(img, save=True)
    if len(list(results[0].boxes.cls)) == 0:
        sob_defect= "Acceptable"
        pob_defect="Acceptable"
        dob_defect= "Acceptable"
        status="Acceptable"
    else:
        result_output = list(set(map(int, list(results[0].boxes.cls))))

        if 5 in result_output:
            dob_defect = "Unacceptable"
            status = "Unacceptable"
        elif 4 in result_output:
            dob_defect = "Marginal"
            status = "Marginal"
        else:
            dob_defect = "Acceptable"

        if 3 in result_output:
            sob_defect="Unacceptable"
            status = "Unacceptable"
        elif 1 in result_output:
            sob_defect="Marginal"
        else:
            sob_defect="Acceptable"

        if 2 in result_output:
            pob_defect = "Unacceptable"
            status = "Unacceptable"
        elif 0 in result_output:
            pob_defect = "Marginal"
        else:
            pob_defect = "Acceptable"

        if status == "" and any(i=="Marginal" for i in [pob_defect, sob_defect, dob_defect]):
            status="Marginal"
        elif status == "":
            status = "Acceptable"
    result["dent"] = dob_defect
    result["pob"] = pob_defect
    result["scuff"] = sob_defect
    
    
    batch_id = request.POST.get('batch_id')
    # sob_defect= "Acceptable"
    # pob_defect="Marginal"
    # dob_defect= "Acceptable"
    # cap_defect="Acceptable"
    # status="Marginal"


    # sob_defect= result[0]["scuff"]
    # pob_defect= result[0]["pob"]
    # dob_defect= result[0]["dent"]
    # cap_defect= "Acceptable"
    # status= result[1]


    time_stamp= time.time()
    bottle_size = request.POST.get('bottle_size')
    
    
    conn = sqlite3.connect("console_database.sqlite3")  
    cursor = conn.cursor()
    cursor.executescript(f"""CREATE TABLE IF NOT EXISTS batches(batch_id INTEGER PRIMARY KEY, date_of_inspection timestamp, status TEXT, bottles_size TEXT, total_bottles INTEGER, sob_defect TEXT, pob_defect TEXT, dob_defect TEXT, cap_defect TEXT);
                CREATE TABLE IF NOT EXISTS bottles_inspection_result(batch_id INTEGER,  sob_defect TEXT, pob_defect TEXT, dob_defect TEXT, cap_defect TEXT, date_of_inspection timestamp, status TEXT, FOREIGN KEY(batch_id) REFERENCES batches(batch_id));
                INSERT INTO batches(batch_id, date_of_inspection, bottles_size) VALUES ({batch_id}, {time_stamp}, '{bottle_size}') ON CONFLICT(batch_id) DO UPDATE SET batch_id = {batch_id};
                INSERT INTO bottles_inspection_result(batch_id,  sob_defect, pob_defect, dob_defect, cap_defect, status, date_of_inspection) VALUES ({batch_id}, '{sob_defect}','{pob_defect}','{dob_defect}','{cap_defect}','{status}', {time_stamp});
                UPDATE batches SET status= CASE WHEN EXISTS(SELECT status FROM bottles_inspection_result WHERE status='Unacceptable' AND batches.batch_id=bottles_inspection_result.batch_id) THEN 'Unacceptable' WHEN NOT EXISTS(SELECT status FROM bottles_inspection_result WHERE status='Unacceptable' AND batches.batch_id=bottles_inspection_result.batch_id) AND EXISTS(SELECT status FROM bottles_inspection_result WHERE status='Marginal'  AND batches.batch_id=bottles_inspection_result.batch_id) THEN 'Marginal'   
                ELSE 'Acceptable' END WHERE batch_id = {batch_id};
                UPDATE batches SET total_bottles= (SELECT COUNT(*) FROM bottles_inspection_result WHERE batches.batch_id=bottles_inspection_result.batch_id);
                UPDATE batches SET sob_defect= CASE WHEN EXISTS(SELECT sob_defect FROM bottles_inspection_result WHERE sob_defect='Unacceptable' AND batches.batch_id=bottles_inspection_result.batch_id) THEN 'Unacceptable' WHEN NOT EXISTS(SELECT sob_defect FROM bottles_inspection_result WHERE sob_defect='Unacceptable' AND batches.batch_id=bottles_inspection_result.batch_id) AND EXISTS(SELECT sob_defect FROM bottles_inspection_result WHERE sob_defect='Marginal' AND batches.batch_id=bottles_inspection_result.batch_id) THEN 'Marginal' ELSE 'Acceptable' END
                WHERE batch_id = {batch_id};
                UPDATE batches SET pob_defect= CASE WHEN EXISTS(SELECT pob_defect FROM bottles_inspection_result WHERE pob_defect='Unacceptable' AND batches.batch_id=bottles_inspection_result.batch_id) THEN 'Unacceptable' WHEN NOT EXISTS(SELECT pob_defect FROM bottles_inspection_result WHERE pob_defect='Unacceptable' AND batches.batch_id=bottles_inspection_result.batch_id) AND EXISTS(SELECT pob_defect FROM bottles_inspection_result WHERE pob_defect='Marginal' AND batches.batch_id=bottles_inspection_result.batch_id) THEN 'Marginal' ELSE 'Acceptable' END
                WHERE batch_id = {batch_id};
                UPDATE batches SET dob_defect= CASE WHEN EXISTS(SELECT dob_defect FROM bottles_inspection_result WHERE dob_defect='Unacceptable' AND batches.batch_id=bottles_inspection_result.batch_id) THEN 'Unacceptable' WHEN NOT EXISTS(SELECT dob_defect FROM bottles_inspection_result WHERE dob_defect='Unacceptable' AND batches.batch_id=bottles_inspection_result.batch_id) AND EXISTS(SELECT dob_defect FROM bottles_inspection_result WHERE dob_defect='Marginal' AND batches.batch_id=bottles_inspection_result.batch_id) THEN 'Marginal' ELSE 'Acceptable' END
                WHERE batch_id = {batch_id}; 
                """)
    conn.commit()
    conn.close()
    
    
    params = {'result': status, 'entries': []}
    for i in result:
        params["entries"].append({'defect_name': i, 'defect_result': result[i]})
    # render(request, "pages/quality_check.html", {'time_taken': (time.time() - progress_time_start)*1000})
    return  render(request, "pages/result_modal_body.html", params)
    # return None



    # this will also get commented out
    # label1 = model1.predict(img)
    # label2 = model2.predict(img)
    # label3 = model3.predict(img)
    
    # will be commented out
    # p1=np.argmax(label1)
    # p2=np.argmax(label2)
    # p3 = np.argmax(label3)

    
    
    # paras = {0: "Acceptable", 1: "marginal", 2: "unacceptable"}
    # par = {0:"cap", 1: "bottle", 2:"dent"}
    # # print(p)
    # # params = {"defect_name": par[0], "defect_result": paras[0]}
    
    # params = {'result': 'Acceptable', 'entries': [{'defect_name': 'Cap Not Seated', 'defect_result': 'Acceptable'}]}




    # para = {"d1": p1, "d2":p2, "d3":p3}
    # para = {"d1": str(p1), "d2": str(p2), "d3":str(p3)}
    # return JsonResponse(para)
    
    # batch_id = 1234
    # sob_defect= "Acceptable"
    # pob_defect="Acceptable"
    # dob_defect= "Acceptable"
    # cap_defect="Marginal"
    # status="Marginal"
    # time_stamp=time()
    # bottle_size = "Medium"
    
        
    # cursor = conn.cursor()
    # cursor.executescript(f"""CREATE TABLE IF NOT EXISTS batches(batch_id INTEGER PRIMARY KEY, date_of_inspection timestamp, status TEXT, bottles_size TEXT);
    #             CREATE TABLE IF NOT EXISTS bottles_inspection_result(batch_id INTEGER,  sob_defect TEXT, pob_defect TEXT, dob_defect TEXT, cap_defect TEXT, status TEXT, FOREIGN KEY(batch_id) REFERENCES batches(batch_id));
    #             INSERT INTO batches(batch_id, date_of_inspection, bottles_size) VALUES ({batch_id}, {time_stamp}, '{bottle_size}') ON CONFLICT(batch_id) DO UPDATE SET batch_id = {batch_id};
    #             INSERT INTO bottles_inspection_result(batch_id,  sob_defect, pob_defect, dob_defect, cap_defect, status) VALUES ({batch_id}, '{sob_defect}','{pob_defect}','{dob_defect}','{cap_defect}','{status}');
    #             UPDATE batches SET status= CASE WHEN EXISTS(SELECT status FROM bottles_inspection_result WHERE status='Unacceptable') THEN 'Unacceptable' WHEN NOT EXISTS(SELECT status FROM bottles_inspection_result WHERE status='Unacceptable') AND EXISTS(SELECT status FROM bottles_inspection_result WHERE status='Marginal') THEN 'Marginal'   
    #             ELSE 'Acceptable' END WHERE batch_id = {batch_id};""")

    # Commit our command
    # conn.commit()
    
    # return JsonResponse({"date": datetime.now(),"date1": datetime.now().strftime('%Y-%m-%d %H:%M:%S'), "time": time.time(),"batch_id": request.POST.get('batch_id')})

def get_batch_report(request):
    
    defect_type = request.POST.get('defect_type')
    time_period = request.POST.get('time_period')
    defect_status = request.POST.get('defect_status')
    
    conn = sqlite3.connect("console_database.sqlite3")  
    cursor = conn.cursor()
    
    
    
    if time_period == "Daily":
        if defect_type == "Dent On Bottle":
            cursor.execute(f"""
            SELECT strftime('%Y-%m-%d 00:00:00', datetime(date_of_inspection, 'unixepoch'))||' GMT+0500', SUM(total_bottles) FROM batches WHERE  dob_defect='{defect_status}' AND strftime('%Y-%m-%d',  datetime(date_of_inspection, 'unixepoch')) >= date('now','-7 days') AND 
            strftime('%Y-%m-%d', datetime(date_of_inspection, 'unixepoch'))<=date('now') GROUP BY strftime('%W-%d', datetime(date_of_inspection, 'unixepoch'))
            """)
        elif defect_type == "Scuff On Bottle":
            cursor.execute(f"""
            SELECT strftime('%Y-%m-%d 00:00:00', datetime(date_of_inspection, 'unixepoch'))||' GMT+0500', SUM(total_bottles) FROM batches WHERE  sob_defect='{defect_status}' AND strftime('%Y-%m-%d',  datetime(date_of_inspection, 'unixepoch')) >= date('now','-7 days') AND 
            strftime('%Y-%m-%d', datetime(date_of_inspection, 'unixepoch'))<=date('now') GROUP BY strftime('%W-%d', datetime(date_of_inspection, 'unixepoch'))
            """)
        else:
            cursor.execute(f"""
            SELECT strftime('%Y-%m-%d 00:00:00', datetime(date_of_inspection, 'unixepoch'))||' GMT+0500', SUM(total_bottles) FROM batches WHERE  pob_defect='{defect_status}' AND strftime('%Y-%m-%d',  datetime(date_of_inspection, 'unixepoch')) >= date('now','-7 days') AND 
            strftime('%Y-%m-%d', datetime(date_of_inspection, 'unixepoch'))<=date('now') GROUP BY strftime('%W-%d', datetime(date_of_inspection, 'unixepoch'))
            """)
    elif time_period == "Monthly":
        if defect_type == "Dent On Bottle":
            cursor.execute(f"""
        SELECT strftime('%Y-%m-%d 00:00:00', datetime(date_of_inspection, 'unixepoch'))||' GMT+0500', SUM(total_bottles) FROM batches WHERE dob_defect='{defect_status}' AND strftime('%Y-%m-%d',  datetime(date_of_inspection, 'unixepoch')) >= date('now','-1 month') AND 
        strftime('%Y-%m-%d', datetime(date_of_inspection, 'unixepoch'))<=date('now') GROUP BY strftime('%m-%W', datetime(date_of_inspection, 'unixepoch'))
        """)
        elif defect_type == "Scuff On Bottle":
            cursor.execute(f"""
        SELECT strftime('%Y-%m-%d 00:00:00', datetime(date_of_inspection, 'unixepoch'))||' GMT+0500', SUM(total_bottles) FROM batches WHERE sob_defect='{defect_status}' AND strftime('%Y-%m-%d',  datetime(date_of_inspection, 'unixepoch')) >= date('now','-1 month') AND 
        strftime('%Y-%m-%d', datetime(date_of_inspection, 'unixepoch'))<=date('now') GROUP BY strftime('%m-%W', datetime(date_of_inspection, 'unixepoch'))
        """)
        else:
            cursor.execute(f"""
        SELECT strftime('%Y-%m-%d 00:00:00', datetime(date_of_inspection, 'unixepoch'))||' GMT+0500', SUM(total_bottles) FROM batches WHERE pob_defect='{defect_status}' AND strftime('%Y-%m-%d',  datetime(date_of_inspection, 'unixepoch')) >= date('now','-1 month') AND 
        strftime('%Y-%m-%d', datetime(date_of_inspection, 'unixepoch'))<=date('now') GROUP BY strftime('%m-%W', datetime(date_of_inspection, 'unixepoch'))
        """)
    else:
        if defect_type == "Dent On Bottle":
            cursor.execute(f"""
        SELECT strftime('%Y-%m-01 00:00:00', datetime(date_of_inspection, 'unixepoch'))||' GMT+0500', SUM(total_bottles) FROM batches WHERE dob_defect='{defect_status}' AND strftime('%Y-%m-%d',  datetime(date_of_inspection, 'unixepoch')) >= date('now','-1 year') AND 
        strftime('%Y-%m-%d', datetime(date_of_inspection, 'unixepoch'))<=date('now') GROUP BY strftime('%Y-%m', datetime(date_of_inspection, 'unixepoch'))
        """)
        elif defect_type == "Scuff On Bottle":
            cursor.execute(f"""
        SELECT strftime('%Y-%m-01 00:00:00', datetime(date_of_inspection, 'unixepoch'))||' GMT+0500', SUM(total_bottles) FROM batches WHERE sob_defect='{defect_status}' AND strftime('%Y-%m-%d',  datetime(date_of_inspection, 'unixepoch')) >= date('now','-1 year') AND 
        strftime('%Y-%m-%d', datetime(date_of_inspection, 'unixepoch'))<=date('now') GROUP BY strftime('%Y-%m', datetime(date_of_inspection, 'unixepoch'))
        """)
        else:
            cursor.execute(f"""
        SELECT strftime('%Y-%m-01 00:00:00', datetime(date_of_inspection, 'unixepoch'))||' GMT+0500', SUM(total_bottles) FROM batches WHERE pob_defect='{defect_status}' AND strftime('%Y-%m-%d',  datetime(date_of_inspection, 'unixepoch')) >= date('now','-1 year') AND 
        strftime('%Y-%m-%d', datetime(date_of_inspection, 'unixepoch'))<=date('now') GROUP BY strftime('%Y-%m', datetime(date_of_inspection, 'unixepoch'))
        """)
    
    data = cursor.fetchall()
    conn.close()
    dat = []

    for i in data:
        dat.append({"x": i[0], "y":i[1]})
        
    return JsonResponse({"data_lst": dat})

def check_batch_info(request):
    batch_id = request.POST.get('batch_id')
    
    conn = sqlite3.connect("console_database.sqlite3")  
    cursor = conn.cursor()
    
    data = cursor.execute(f"""
                        SELECT dob_defect, sob_defect, pob_defect from bottles_inspection_result WHERE batch_id={batch_id}                 
                          """)
    data = data.fetchall()
    conn.close()
    # iter over data
    params = {'result': "", 'entries': []}
    result = []
    for i in data:
        dat = {}
        dat["dob"] = i[0]
        dat["sob"] = i[1]
        dat["pob"] = i[2]
        if all(j=="Acceptable" for j in i):
            result.append("Acceptable")
            dat["res"] = "Acceptable"
        elif any(j=="Unacceptable" for j in i):
            result.append("Unacceptable")
            dat["res"] = "Unacceptable"
        else:
            result.append("Marginal")
            dat["res"] = "Marginal"
        params["entries"].append(dat)
        
            
    if all(j=="Acceptable" for j in result):
        params['result'] = "Acceptable"
    elif any(j=="Unacceptable" for j in i):
        params['result'] = "Unacceptable"
    else:
        params['result'] = "Marginal"
            
    # render(request, "pages/quality_check.html", {'time_taken': (time.time() - progress_time_start)*1000})
    return  render(request, "pages/batch_popup.html", params)

def report_data_generation(request):
    defect_type = request.POST.get('defect_type')
    time_period = request.POST.get('time_period')
    defect_status = request.POST.get('defect_status')

    conn = sqlite3.connect("console_database.sqlite3")  
    cursor = conn.cursor()

    if defect_type=='Dent On Bottle':
        defect_type = 'dob_defect'
    elif defect_type=='Scuff On Bottle':
        defect_type = 'sob_defect'
    else:
        defect_type = 'pob_defect'

    if time_period=='Daily':
        time_period = ['-7 days', '%W-%d']
    elif time_period=='':
        time_period = ['-1 month', '%m-%W']
    else:
        time_period = ['-1 year', '%Y-%m']
    
    batch_data = cursor.execute(f"""
        SELECT batch_id, bottles_size, {defect_type}, status, 
        case strftime('%m', datetime(date_of_inspection, 'unixepoch', 'localtime')) when '01' then 'Jan' when '02' then 'Feb' when '03' then 'March' when '04' then 'April' when '05' then 'May' when '06' then 'June' when '07' then 'July' when '08' then 'Aug' when '09' then 'Sept' when '10' then 'Oct' when '11' then 'Nov' when '12' then 'Dec' else '' end
        || strftime(' %d, %Y, %H:%M:%S', datetime(date_of_inspection, 'unixepoch', 'localtime'))
        FROM batches WHERE {defect_type}='{defect_status}' AND strftime('%Y-%m-%d',  datetime(date_of_inspection, 'unixepoch')) >= date('now','{time_period[0]}') AND 
        strftime('%Y-%m-%d', datetime(date_of_inspection, 'unixepoch'))<=date('now')
         """)
    
    batch_data = list(map(lambda x: list(x), batch_data))
    conn.close()
    params = {"batch_data": batch_data}
    return JsonResponse(params)

def get_weeks_between_dates(start_date, end_date):
    weeks = []
    current_date = start_date

    # Adjust start_date to the first day of the week
    current_date -= timedelta(days=current_date.weekday())

    while current_date <= end_date:
        weeks.append(datetime.datetime.strptime(current_date, "%W/%Y"))
        current_date += timedelta(weeks=1)

    return weeks

def get_months_between_dates(start_date, end_date):
    start_month = start_date.month
    start_year = start_date.year

    months = []

    while start_date <= end_date:
        months.append(start_date.strftime("%b %Y"))
        start_date += relativedelta(months=1)

    return months

def get_years_between_dates(start_date, end_date):
    start_year = start_date.year
    end_year = end_date.year

    years = list(map(str, list(range(start_year, end_year + 1))))

    return years

def data_change_on_date(request):
    
    start_date = request.POST.get('date_start')
    end_date = request.POST.get('date_end')
    label = request.POST.get('range_label')
    date_format = "%Y-%m-%d"
    start_time = datetime.datetime.strptime(start_date, date_format)
    end_time = datetime.datetime.strptime(end_date, date_format)
    time_difference = end_time - start_time
    grouper = ""
    
    
    
    today = date.today()
    Dateslist = []
    
    conn = sqlite3.connect("console_database.sqlite3")  
    cursor = conn.cursor()
    
    if label=="Today" or label=="Yesterday":
        grouper = "%H"
        date_format = "%H:00"
        Dateslist = [datetime.time(i).strftime('%H:00') for i in range(24)]
    elif label=="Last 7 Days" or label=="Last 30 Days" or label=="This Month" or label=="Last Month":
        grouper = "%d"
        date_format = "%d/%m"
        for i in range(time_difference.days + 1):
            Dateslist.append(datetime.datetime.strptime(start_date + timedelta(days=i), date_format))
    elif label=="Custom Range":
        if time_difference==1 or time_difference==0:
            grouper = "%H"
            date_format = "%H:00"
            Dateslist = [datetime.time(i).strftime('%H:00') for i in range(24)]
        elif time_difference<=31 and time_difference>1:
            grouper = "%d"
            date_format = "%d/%m"
            for i in range(time_difference.days + 1):
                Dateslist.append(datetime.datetime.strptime(start_date + timedelta(days=i), date_format))
        elif time_difference//7 <= 15:
            grouper = "%W"
            date_format = "%W/%Y"
            Dateslist = get_weeks_between_dates(start_time, end_time)
        elif time_difference//30 <= 24:
            grouper = "%m"
            date_format = "%b %Y"
            Dateslist = get_months_between_dates(start_time, end_time)
        else:
            grouper = "%Y"
            date_format = "%Y"
            Dateslist = get_years_between_dates(start_time, end_time)
    line_chart_result = cursor.execute(f"""
                select COUNT(CASE WHEN status="Acceptable" THEN 1 END), COUNT(CASE WHEN status="Marginal" THEN 1 END), 
                COUNT(CASE WHEN status="Unacceptable" THEN 1 END), strftime('{date_format}',  datetime(date_of_inspection, 'unixepoch')) as 'month-year' 
                from bottles_inspection_result WHERE strftime("%Y-%m-%d", datetime(date_of_inspection, 'unixepoch')) BETWEEN '{start_date}' AND 
                '{end_date}'  group by strftime('{grouper}',  datetime(date_of_inspection, 'unixepoch'));
                """)
    
    # To Do Work from here on :(
    
    line_chart_result = line_chart_result.fetchall()
    line_chart_result_accept = []
    line_chart_result_margin = []
    line_chart_result_unaccept = []
    count = 0
    for i in range(len(Dateslist)):

        for j in line_chart_result:
            if j[-1] == str(Dateslist[i]):
                line_chart_result_accept.append(j[0])
                line_chart_result_unaccept.append(j[2])
                line_chart_result_margin.append(j[1])
                count += 1
                break
        # Dateslist[i] = "/".join(Dateslist[i].split("-")[-1:0:-1])
        if count > 0:
            count = 0
            continue
        line_chart_result_accept.append(0)
        line_chart_result_unaccept.append(0)
        line_chart_result_margin.append(0)

        


    # Fetching the percentages of the status / Pie Chart
    pie_chart_result = cursor.execute("""
                    select ROUND((COUNT(CASE WHEN status="Acceptable" THEN 1 END)* 100/COUNT(*)), 2), ROUND((COUNT(CASE WHEN status="Marginal" THEN 1 END) * 100/COUNT(*)) , 2), 
                    ROUND((COUNT(CASE WHEN status="Unacceptable" THEN 1 END)* 100/COUNT(*)) , 2)
                    from bottles_inspection_result WHERE strftime("%Y-%m-%d", datetime(date_of_inspection, 'unixepoch')) BETWEEN '{start_date}' AND 
                    '{end_date}';
                """)
    pie_chart_result = list(pie_chart_result.fetchone()) #(% of acceptable, % of marginal, % of unacceptable)
    
    
    # Fetching the individual counts of defect status/type in the current month

    # For Acceptable
    acceptable_count_bottles = cursor.execute("""SELECT Count(*) FROM bottles_inspection_result WHERE status='Acceptable' AND strftime("%Y-%m-%d", datetime(date_of_inspection, 'unixepoch')) BETWEEN '{start_date}' AND 
                '{end_date}';""")
    acceptable_count_bottles = list(acceptable_count_bottles.fetchone())
    # For Marginal
    marginal_count_bottles = cursor.execute("""SELECT Count(*) FROM bottles_inspection_result WHERE status='Marginal' AND strftime("%Y-%m-%d", datetime(date_of_inspection, 'unixepoch')) BETWEEN '{start_date}' AND 
                '{end_date}';""")
    marginal_count_bottles = list(marginal_count_bottles.fetchone())
    # For Unacceptable
    unacceptable_count_bottles = cursor.execute("""SELECT Count(*) FROM bottles_inspection_result WHERE status='Unacceptable' AND strftime("%Y-%m-%d", datetime(date_of_inspection, 'unixepoch')) BETWEEN '{start_date}' AND 
                '{end_date}' """)
    unacceptable_count_bottles = list(unacceptable_count_bottles.fetchone())
    # For total bottles
    total_count_bottles = cursor.execute("""SELECT Count(*) FROM bottles_inspection_result WHERE strftime("%Y-%m-%d", datetime(date_of_inspection, 'unixepoch')) BETWEEN '{start_date}' AND 
                '{end_date}' """)
    total_count_bottles = list(total_count_bottles.fetchone())
    
    conn.close()
    total_bottles = 1
    if total_count_bottles[0] != 0:
        total_bottles = total_count_bottles[0]
    
    params = {"line_chart_accept_results": line_chart_result_accept, "line_chart_unaccept_results": line_chart_result_unaccept, 
              "line_chart_marginal_results": line_chart_result_margin, "pie_chart_results": pie_chart_result,
              "acceptable_count_bottles": acceptable_count_bottles[0], "unacceptable_count_bottles": unacceptable_count_bottles[0],
              "marginal_count_bottles": marginal_count_bottles[0], "total_count_bottles": total_count_bottles[0], "date_range_chart": Dateslist,
              "percent_acceptable": int((acceptable_count_bottles[0]/total_bottles)*100), "percent_unacceptable": int((unacceptable_count_bottles[0]/total_bottles)*100),
              "percent_marginal": int((marginal_count_bottles[0]/total_bottles)*100),
              }

    return JsonResponse(params)