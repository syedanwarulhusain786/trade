from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect 
# Create your tests here.
from django.core.paginator import Paginator

from django.contrib import messages
from django.shortcuts import render, redirect 

from django.db.models import Q

from django.utils.translation import gettext as _
from django.shortcuts import render

# Create your views here.
from django.shortcuts import render


# from accounts.serializers import *
import time


import datetime
from django.db.models import Q
from datetime import datetime, timedelta
from bs4 import BeautifulSoup
from django.http import HttpResponse
from django.http import JsonResponse
from django.contrib import messages
from .models import Data
# Create your views here.
# views.py

import re

def get_date(forward, backward):
    # Implement your CSV merging logic here
    # You can use the csv module to read and merge the data from the two files
    # Example logic (for a text file):
    with forward.open() as file_content:
            forwardcontent = file_content.read().decode('utf-8')
    with backward.open() as file_content:
            backwardcontent = file_content.read().decode('utf-8')
    soup1 = BeautifulSoup(forwardcontent, 'xml')
    soup2 = BeautifulSoup(backwardcontent, 'xml')
    forward_title=soup1.find('Title').text.split('M1')[-1].strip()
    forward_date=forward_title.split('-')
    forward_date_start=forward_date[0]
    forward_date_end=forward_date[1]
    backward_title=soup2.find('Title').text.split('M1')[-1].strip()
    # backward_date=backward_title.split('-')
    # backward_date_start=backward_date[0]
    # backward_date_end=backward_date[0]
    if forward_title==backward_title:
        date_str = re.search(r'\d{4}.\d{2}.\d{2}', forward_date_start)
        date_str1 = re.search(r'\d{4}.\d{2}.\d{2}', forward_date_end)
        
        if date_str and date_str1:
            start =forward_date_start.replace(".","-")#datetime.strptime(date_str.group(), '%Y.%m.%d')
            end =forward_date_end.replace(".","-")#datetime.strptime(date_str1.group(), '%Y.%m.%d')
            
        dt={
            'start':start,
            'end':end,
            
        }
        return dt
    else:
        return  dt
def get_rows_back(soup):
    data={}
    back_head=soup.find('Row').find_all("ss:Cell")
    back_pass=back_head[0].text
    back_result=back_head[1].text.replace(' ','_')
    back_profit=back_head[2].text.replace(' ','_')
    back_r_f=back_head[5].text.replace(' ','_')
    back_e_dd_per=back_head[8].text.replace(' ','_').replace('%','')
    back_trades=back_head[9].text.replace(' ','_')
    for d in soup.find_all('Row')[1:]:
        dt = d.find_all("Cell")
        data[dt[0].text]={
            f"back_pass":dt[0].text,
            f"back_{back_result}":dt[1].text,
            f"back_{back_profit}":dt[2].text,
            f"back_{back_r_f}":dt[5].text,
            f"back_{back_e_dd_per}d":dt[8].text,
            f"back_{back_trades}":dt[9].text,
        }
        
    return data

def get_rows_forwad(soup,res,diff,file_name,user_ip):
    deposit=100000
    ok_dd=1000
    # print(ok_dd)
    data=[]
    forward_head=soup.find('Row').find_all("ss:Cell")
    forward_pass=forward_head[0].text
    forward_result=forward_head[1].text.replace(' ','_')
    forward_profit=forward_head[3].text.replace(' ','_')
    forward_r_f=forward_head[6].text.replace(' ','_')
    forward_e_dd_per=forward_head[9].text.replace(' ','_').replace('%','')
    forward_trades=forward_head[10].text.replace(' ','_')
    for d in soup.find_all('Row')[1:]:
        dt = d.find_all("Cell")
        if dt[0].text.strip() in res :#and dt[0].text.strip() =='7703':
            res[dt[0].text][f"ips"]=user_ip
            
            res[dt[0].text][f"filename"]=file_name
            res[dt[0].text][f"forward_{forward_result}"]=dt[1].text
            res[dt[0].text][f"forward_{forward_profit}"]=dt[3].text
            res[dt[0].text][f"forward_{forward_r_f}"]=dt[6].text
            res[dt[0].text][f"forward_{forward_e_dd_per}d"]=dt[9].text
            res[dt[0].text][f"forward_{forward_trades}"]=dt[10].text
            try:
                # print(float(dt[3].text),float(res[dt[0].text]['back_Profit']),diff)
                res[dt[0].text][f"profit_match"]=round((float(dt[3].text)/(float(res[dt[0].text]['back_Profit'])/diff))*100,2)
            except:
                res[dt[0].text][f"profit_match"]=0
            try:
                res[dt[0].text][f"total_profit"]=float(dt[3].text)+float(res[dt[0].text]['back_Profit'])
            except:
                res[dt[0].text][f"total_profit"]=0
            try:
                res[dt[0].text][f"max_original_dd"]=round((float(res[dt[0].text]['back_Equity_DD_']))*(deposit/100),2)
                
            except:
                res[dt[0].text][f"max_original_dd"]=0

            data.append(res[dt[0].text])   
             
            
    return data

def merge_xml(file1, file2,diff,file_name,user_ip):
            # Implement your CSV merging logic here
        # You can use the csv module to read and merge the data from the two files
        soup1 = BeautifulSoup(file1, 'xml')
        soup2 = BeautifulSoup(file2, 'xml')

        # Implement your merging logic here
        
        
        # For demonstration purposes, we'll just concatenate the XML strings
        merged_xml_data = get_rows_back(soup2)
        time.sleep(10)
        
        merged_xml_data = get_rows_forwad(soup1,merged_xml_data,diff,file_name,user_ip)
        time.sleep(10)
        
        # Example:
        # Read file1 and file2 and merge the data into merged_data

        return merged_xml_data
q_objects=''    
    
def calculation(date2_str,date1_str):
    # Convert the date strings to datetime objects
    date1 = datetime.strptime(date1_str, '%Y-%m-%d')
    date2 = datetime.strptime(date2_str, '%Y-%m-%d')

    # Calculate the difference in days between the two dates
    date_difference = (date2 - date1).days

    # Calculate the number of weeks
    weeks = date_difference / 7
    return weeks
def test(request):
    global q_objects
    merged_data = [] 
    file_name=''
    user_ip = request.META.get('REMOTE_ADDR', None)
    print(user_ip)
    if request.method == 'POST' and 'clear1' in request.POST:
        
        Data.objects.filter(ips=user_ip).delete()
        forward_uploaded_file = request.FILES.get('fileforward')
        backward_uploaded_file = request.FILES.get('filebackward')
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        forward_date = request.POST.get('forward')
        
        # Check if both files were uploaded
        if not forward_uploaded_file or not backward_uploaded_file:
            messages.success(request,"Both forward and backward files are required.")
            return redirect('sitefinder')
        # Check if the uploaded files are XML files
        if not forward_uploaded_file.name.endswith('.xml') or not backward_uploaded_file.name.endswith('.xml'):
            messages.success(request,"Both files must be XML files.")
            return redirect('sitefinder')
        g15 = calculation(forward_date, start_date)
        g16 = calculation(end_date, forward_date)
        g17 = g15 / g16
        file_name = forward_uploaded_file.name.split('.')[0]

        merged_data = merge_xml(forward_uploaded_file, backward_uploaded_file, g17,file_name,user_ip)
        instances_to_save = [Data(**entry) for entry in merged_data]

        # Use bulk_create to save all instances in one go
        Data.objects.bulk_create(instances_to_save)
        messages.success(request,"Data is Saved SuccessFully")
    
    merged = Data.objects.all()

    return render(request, 'test.html', {'pages': merged,'filename':file_name,})


import json
def upload_file(request):
    global extracted_date
    if request.method == 'POST':
        json_data = json.loads(request.body)

        # Now you can access and manipulate the JSON data as needed
        # For example, print it to the console

        # forward_uploaded_file = request.FILES['fileforward']
        # backward_uploaded_file = request.FILES['filebackward']
        
        # Extract the date from the uploaded file
        # extracted_date = get_date(forward_uploaded_file,backward_uploaded_file)
        # You can now use the extracted_date as needed, e.g., save it to a model or perform other actions.
        
        # For demonstration purposes, we'll return the extracted date as an HTTP response.
        return JsonResponse({"start_date":"false"})

    


















# class MergeCSV(APIView):
#     parser_class = (FileUploadParser,)
#     parser_class = (FileUploadParser,)

#     def post(self, request):
        
#         file1 = request.data.get('file1')
#         file2 = request.data.get('file2')
#         if file1.name.find('forward'):
#             forward=file1.read()
#             backward=file2.read()
#         elif file2.name.find('forward'):
#             forward=file2.read() 
#             backward=file1.read()
#         else:
#             return Response({'error': 'Atleast one XML files should be forward.'}, status=status.HTTP_400_BAD_REQUEST)
#         # Check if both files are provided
#         if not file1 or not file2:
#             return Response({'error': 'Both XML files are required.'}, status=status.HTTP_400_BAD_REQUEST)



#         dt = get_date(forward,backward)
#         print(dt)
#         # Read and merge XML files
#         # merged_data = self.merge_xml(forward, backward)

#         # Serialize the merged data
#         # serializer = DataEntrySerializer(data=merged_data, many=True)
#         # if serializer.is_valid():
#         #     serializer.save()
#         #     return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(dt, status=status.HTTP_400_BAD_REQUEST)

#     def merge_xml(self, file1, file2):
#         # Implement your CSV merging logic here
#         # You can use the csv module to read and merge the data from the two files
#         soup1 = BeautifulSoup(file1, 'xml')
#         soup2 = BeautifulSoup(file2, 'xml')

#         # Implement your merging logic here
        
        
#         # For demonstration purposes, we'll just concatenate the XML strings
#         merged_xml_data = get_rows_back(soup2)
#         print(len(merged_xml_data))
#         time.sleep(10)
        
#         merged_xml_data = get_rows_forwad(soup1,merged_xml_data)
#         time.sleep(10)
#         print(len(merged_xml_data))
        
#         # Example:
#         # Read file1 and file2 and merge the data into merged_data

#         return merged_xml_data

# def get_rows_back(soup):
#     data={}
#     back_head=soup.find('Row').find_all("ss:Cell")
#     back_pass=back_head[0].text
#     back_result=back_head[1].text
#     back_profit=back_head[2].text
#     back_r_f=back_head[5].text
#     back_e_dd_per=back_head[8].text
#     back_trades=back_head[9].text
#     for d in soup.find_all('Row')[1:]:
#         dt = d.find_all("Cell")
        
#         data[dt[0].text]={
#             f"back_{back_result}":dt[1].text,
#             f"back_{back_profit}":dt[2].text,
#             f"back_{back_r_f}":dt[5].text,
#             f"back_{back_e_dd_per}":dt[8].text,
#             f"back_{back_trades}":dt[9].text,
#         }
    
#     return data

# def get_rows_forwad(soup,res):
#     data={}
#     forward_head=soup.find('Row').find_all("ss:Cell")
#     forward_pass=forward_head[0].text
#     forward_result=forward_head[1].text
#     forward_profit=forward_head[3].text
#     forward_r_f=forward_head[6].text
#     forward_e_dd_per=forward_head[9].text
#     forward_trades=forward_head[10].text
#     for d in soup.find_all('Row')[1:]:
#         dt = d.find_all("Cell")
#         data[dt[0].text]={**res[dt[0].text], **{f"forward_{forward_result}":dt[1].text,f"forward_{forward_profit}":dt[2].text,f"forward_{forward_r_f}":dt[5].text,f"forward_{forward_e_dd_per}":dt[8].text,f"forward_{forward_trades}":dt[9].text,}}
#         print(data[dt[0].text])
#     return data


# def get_date(forward, backward):
#     # Implement your CSV merging logic here
#     # You can use the csv module to read and merge the data from the two files
#     soup1 = BeautifulSoup(forward, 'xml')
#     soup2 = BeautifulSoup(backward, 'xml')
#     forward_title=soup1.find('Title').text.split('M1')[-1].strip()
#     forward_date=forward_title.split('-')
#     forward_date_start=forward_date[0]
#     forward_date_end=forward_date[1]
#     backward_title=soup2.find('Title').text.split('M1')[-1].strip()
#     backward_date=backward_title.split('-')
#     backward_date_start=backward_date[0]
#     backward_date_end=backward_date[0]
#     if forward_title==backward_title:
#         dt=[{
#             'forward_date_start':forward_date_start,
#             'forward_date_end':forward_date_end,
#             'backward_date_start':backward_date_start,
#             'backward_date_end':backward_date_end,
#         }]
#         print(dt)
#         return Response(dt, status=status.HTTP_200_OK)
#     else:
#         return  Response(False, status=status.HTTP_400_BAD_REQUEST)
