from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from rest_framework.views import APIView
from .models import *
from rest_framework.response import Response
from .serializer import *
from django.http import HttpResponse
from . serializer import *
from .utils import get_db_handle, get_collection_handle
from mongo_auth.permissions import AuthenticatedOnly
import json
from bson import ObjectId
from django.contrib.auth import authenticate, login,logout

class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        return json.JSONEncoder.default(self, o)



# Create your views here.
class MyView(APIView):
    permission_classes = [AuthenticatedOnly]

    def post(self,request):
        try:
            print(request.user)  # This is where magic happens
            username = request.data['user_name']
            password = request.data['password']
            type = request.data['type']
            user = authenticate(request, username=username, password=password)
            print(user)
            resp = False
            if user is not None:
                res = login(request, user)
                print('res',res)
                resp = True
                return Response(status=status.HTTP_200_OK,data={"data": (resp)})

            else:
                print('No user')
                return Response(resp)

        except:
            return Response(status=status.HTTP_404_NOT_FOUND)


    def logout_view(request):
        logout(request)

class ReactView(APIView):
    serializer_class = ReactSerializer

    # db_handle = get_db_handle()
    # collection_handle = get_collection_handle(db_handle, 'personal_users')

    def get(self, request):
        print('request',request.GET['user_name'])
        collection_handle = get_db_handle()
        users = collection_handle.find()
        col = [{'username':u['user_name']} for u in users]
        myquery = {"user_name": request.GET['user_name']}
        mydoc = collection_handle.find(myquery)
        user = []
        for x in mydoc:
            x['_id'] = str(x['_id'])
            user.append(x)
        print(user)
        response = 1 if(len(user)==1) else 0
        print(json.dumps(user))
        return Response(user)

    def post(self, request):
        serializer = ReactSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)

