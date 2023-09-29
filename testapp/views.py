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

from django.http import JsonResponse
from django.template.loader import render_to_string
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
    back_head=soup['heading'][0:32]
    
    back_pass=back_head[0]
    back_result=back_head[2].replace(' ','_')
    back_profit=back_head[3].replace(' ','_')
    back_r_f=back_head[6].replace(' ','_')
    back_e_dd_per=back_head[9].replace(' ','_').replace('%','')
    back_trades=back_head[10].replace(' ','_')
    for dt in soup['data']:
        data[dt['Pass']]={
            f"back_pass":dt['Pass'],
            f"back_{back_result}":dt['Back Result'],
            f"back_{back_profit}":dt['Profit'],
            f"back_{back_r_f}":dt['Recovery Factor'],
            f"back_{back_e_dd_per}d":dt['Equity DD %'],
            f"back_{back_trades}":dt['Trades'],
        }
    return data

def get_rows_forwad(soup,res,diff,file_name,balance,drawdown):
    deposit=balance
    
    # ok_dd=1000
    # print(ok_dd)
    data=[]
    # print(soup['data'][0])
    forward_head=soup['heading'][0:32]
    forward_pass=forward_head[0]
    forward_result=forward_head[1].replace(' ','_')
    forward_profit=forward_head[2].replace(' ','_')
    forward_r_f=forward_head[5].replace(' ','_')
    forward_e_dd_per=forward_head[8].replace(' ','_').replace('%','')
    forward_trades=forward_head[9].replace(' ','_')
    for dt in soup['data']:
        Mypass=dt['Pass'].strip()

        
        
        if dt['Pass'].strip() in res :#and dt[0].text.strip() =='7703':
            res[Mypass][f"filename"]=file_name
            res[Mypass][f"forward_{forward_result}"]=dt['Result']
            res[Mypass][f"forward_{forward_profit}"]=dt['Profit']
            res[Mypass][f"forward_{forward_r_f}"]=dt['Recovery Factor']
            res[Mypass][f"forward_{forward_e_dd_per}d"]=dt['Equity DD %']
            res[Mypass][f"forward_{forward_trades}"]=dt['Trades']
            try:
                # print(float(dt[3].text),float(res[dt[0].text]['back_Profit']),diff)
                res[Mypass][f"profit_match"]=round((float(dt['Profit'])/(float(res[Mypass]['back_Profit'])/diff))*100,2)
            except:
                res[Mypass][f"profit_match"]=0
            try:
                res[Mypass][f"total_profit"]=float(dt['Profit'])+float(res[Mypass]['back_Profit'])
            except:
                res[Mypass][f"total_profit"]=0
            try:
                
                res[Mypass][f"max_original_dd"]=round((float(res[Mypass]['back_Equity_DD_d']))*(deposit/100),2)
                
            except:
                res[Mypass][f"max_original_dd"]=0
                
                
            try:
                res[Mypass][f"Lot_Multiple"]=round(drawdown/round((float(res[Mypass]['back_Equity_DD_d']))*(deposit/100),2),2)
                
            except:
                res[Mypass][f"Lot_Multiple"]=0
            try:
                res[Mypass][f"Estimated_Total_DD"]=round(drawdown/round((float(res[Mypass]['back_Equity_DD_d']))*(deposit/100),2),2)*round((float(res[Mypass]['back_Equity_DD_d']))*(deposit/100),2)
                
            except:
                res[Mypass][f"Estimated_Total_DD"]=0
                
            try:
                res[Mypass][f"Estimated_Profit"]=(float(dt['Profit'])+float(res[Mypass]['back_Profit']))*round(drawdown/round((float(res[Mypass]['back_Equity_DD_d']))*(deposit/100),2),2)
                
            except:
                res[Mypass][f"Estimated_Profit"]=0
            try:
                res[Mypass][f"Max_DD"]=(max(float(res[Mypass]['back_Equity_DD_d']), float(dt['Equity DD %']))*balance)/(100*round(drawdown/round((float(res[Mypass]['back_Equity_DD_d']))*(deposit/100),2),2))
                    
            except:
                res[Mypass][f"Max_DD"]=0

            data.append(res[Mypass])   
        
    return data

def merge_xml(file1, file2,diff,file_name,balance,drawdown):
            # Implement your CSV merging logic here
        # You can use the csv module to read and merge the data from the two files
        # soup1 = BeautifulSoup(file1, 'xml')
        # soup2 = BeautifulSoup(file2, 'xml')

        # Implement your merging logic here
        
        
        # For demonstration purposes, we'll just concatenate the XML strings
        merged_xml_data = get_rows_back(file1)
        merged_xml_data = get_rows_forwad(file2,merged_xml_data,diff,file_name,balance,drawdown)
        # time.sleep(10)
        
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

    return render(request, 'test.html')


import json
def upload_file(request):
    merged_data = [] 
    file_name=''
    global extracted_date
    if request.method == 'POST':

        json_data = json.loads(request.body)
        forward_date=json_data[2]['forward']
        start_date=json_data[2]['start_date']
        end_date=json_data[2]['end_date']
        balance=float(json_data[2]['balance'])
        
        drawdown=float(json_data[2]['drawdown'])
        
        g15 = calculation(forward_date, start_date)
        g16 = calculation(end_date, forward_date)
        g17 = g15 / g16
        file_name = json_data[2]['filename'].split('.')[0]
        merged_data = merge_xml(json_data[1], json_data[0], g17,file_name,balance,drawdown)
        # For demonstration purposes, we'll return the extracted date as an HTTP response.
        return JsonResponse({"page":merged_data})

    


















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
