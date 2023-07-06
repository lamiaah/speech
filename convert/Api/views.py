from rest_framework import status ,generics 
from convert.models import Convert
from convert.Api.serializers import ConvertSerializers
from rest_framework.response import Response
from rest_framework.decorators import api_view
from convert import process ,test
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.shortcuts import render ,redirect
import json


@csrf_exempt
@api_view(['GET','POST'])
def apirecord(request,format =None ):
 
  # ////////////////////////////////////////
  if request.method == 'GET':
    samples = Convert.objects.last()
    # serializer= ConvertSerializers(samples , many= False)
    return Response(samples,status = status.HTTP_200_OK) 
  #  upload file 
  
  if request.method =='POST':
    # request=request.data.copy()
  
    serializer = ConvertSerializers(data= request.data)
  
 
    if serializer.is_valid():
      serializer.save()
      # pass obj to (speech to text) process
      process.file(serializer.data['id'])

      samples = Convert.objects.last()
      # return text in response
      serializer = ConvertSerializers(samples , many= False)
      return Response(serializer.data) 

    else:
       return Response(samples, status = status.HTTP_201_CREATED)
    return Response(  status = status.HTTP_400_BAD_REQUEST)
  

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json



my_list =[]
counter =0
@csrf_exempt
@api_view(['GET','POST'])
def add(request,format =None ):
    
    global my_list

    global counter
    # print(request) 
    # print(request.headers)
    # print(request.body)
    if request.method == 'GET':
      samples = Convert.objects.last()
     
      x=samples.exported_file
      y = x
      x =''
    
      # serializer= ConvertSerializers(samples , many= False)
      return Response(y) 
     

    if request.method == 'POST':
        # f= request.headers
        data = request.body
        # print(data)
        if len(my_list) < 6:
           my_list.append(data)

        else :
           my_list = my_list[1:]
           my_list.append(data)
           x= b''.join(my_list)
         
          #  my_list.clear()
          #  process.file(x)
           test.file(x)
           my_list.clear()


        # if(counter ==2):
        #   # process.file(payloadarray)
        #   # print("done")
        #   # byte_array = bytearray(int(x, 16) for x in my_list)
        #   x= b''.join(my_list)
        #   # print(x)
        #   # with open('speech.wav', mode='wb') as f:
        #   #    f.write(x)
        #   #   #  print("file done")
        #   #    xx='speech.wav'
        #   process.file(x)
        #   counter =0
        #   my_list=[]
        # else:
          
        #   my_list.append(data)
        #   counter +=1
          # print([type(i) for i in my_list])
        # print(my_list)
        # print("counter  " + str(counter))

        return Response(status = status.HTTP_201_CREATED)
    else:
        return Response(status = status.HTTP_400_BAD_REQUEST)


