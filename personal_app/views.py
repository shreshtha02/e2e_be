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
from rest_framework.decorators import api_view
from mongo_auth.utils import create_unique_object_id, pwd_context
from mongo_auth.db import database, auth_collection, fields, jwt_life, jwt_secret, secondary_username_field
import jwt
import datetime
from mongo_auth import messages
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import ValidationError


class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        return json.JSONEncoder.default(self, o)


@api_view(["POST"])
def signup(request):
        try:
            data = request.data if request.data is not None else {}
            signup_data = {"id": create_unique_object_id()}
            all_fields = set(fields + ("email", "password"))
            if secondary_username_field is not None:
                all_fields.add(secondary_username_field)
            for field in set(fields + ("email", "password")):
                if field in data:
                    signup_data[field] = data[field]
                else:
                    return Response(status=status.HTTP_400_BAD_REQUEST,
                                    data={"error_msg": field.title() + " does not exist."})
            signup_data["password"] = pwd_context.hash(signup_data["password"])
            if database[auth_collection].find_one({"email": signup_data['email']}) is None:
                if secondary_username_field:
                    if database[auth_collection].find_one(
                            {secondary_username_field: signup_data[secondary_username_field]}) is None:
                        database[auth_collection].insert_one(signup_data)
                        res = {k: v for k, v in signup_data.items() if k not in ["_id", "password"]}
                        return Response(status=status.HTTP_200_OK,
                                        data={"data": res})
                    else:
                        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED,
                                        data={"data": {
                                            "error_msg": messages.user_exists_field(secondary_username_field)}})
                else:
                    database[auth_collection].insert_one(signup_data)
                    res = {k: v for k, v in signup_data.items() if k not in ["_id", "password"]}
                    return Response(status=status.HTTP_200_OK,
                                    data={"data": res})
            else:
                return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED,
                                data={"data": {"error_msg": messages.user_exists}})
        except ValidationError as v_error:
            return Response(status=status.HTTP_400_BAD_REQUEST,
                            data={'success': False, 'message': str(v_error)})
        except Exception as e:
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            data={"data": {"error_msg": str(e)}})

@api_view(["POST"])
def login(request):
        print('login')
        try:
            data = request.data if request.data is not None else {}
            username = data['username']
            password = data['password']
            type = data['type']
            if "@" in username:
                user = database[auth_collection].find_one({"email": username}, {"_id": 0})
                print(user['type'])
            else:
                if secondary_username_field:
                    user = database[auth_collection].find_one({secondary_username_field: username}, {"_id": 0})
                else:
                    return Response(status=status.HTTP_403_FORBIDDEN,
                                    data={"data": {"error_msg": messages.user_not_found}})
            if user is not None:
                if pwd_context.verify(password, user["password"]):
                    token = jwt.encode({'id': user['id'],
                                        'exp': datetime.datetime.now() + datetime.timedelta(
                                            days=jwt_life)},
                                       jwt_secret, algorithm='HS256')
                    return Response(status=status.HTTP_200_OK,
                                    data={"data": {"token": token,"user":user}})
                else:
                    return Response(status=status.HTTP_403_FORBIDDEN,
                                    data={"error_msg": messages.incorrect_password})
            else:
                return Response(status=status.HTTP_403_FORBIDDEN,
                                data={"data": {"error_msg": messages.user_not_found}})
        except ValidationError as v_error:
            return Response(status=status.HTTP_400_BAD_REQUEST,
                            data={'success': False, 'message': str(v_error)})
        except Exception as e:
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            data={"data": {"error_msg": str(e)}})


###jean countdown
@api_view(["GET"])
def get_countdown(request):
        print('get_countdown')
        try:
            data = request.data if request.data is not None else {}

            # start = datetime.datetime.strptime('12-01-2021', '%m-%d-%Y')
            # end = datetime.datetime.strptime(data['date'], '%m-%d-%Y')
            
            # collection = database[auth_collection].find({'date':{'$gte':start,'$lte':end}})
            collection = database[auth_collection].find()
            print('collection',collection)

            if (collection.count() >0):
                return Response(status=status.HTTP_200_OK,
                                    data={"data": collection})
            else:
                collection = [{"vimeo_id": "xyz","vimeo_link": "https://vimeo.com/324168514","created_at": "2021-12-05","text_msg": "text msg 1","date": "12-01-2021"},{"vimeo_id": "yhn","vimeo_link": "https://vimeo.com/324168514","created_at": "2021-12-05","text_msg": "Text msg 2","date": "12-02-2021"}]
                return Response(status=status.HTTP_200_OK,
                                    data={"data": collection})

        except ValidationError as v_error:
            return Response(status=status.HTTP_400_BAD_REQUEST,
                            data={'success': False, 'message': str(v_error)})
        except Exception as e:
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            data={"data": {"error_msg": str(e)}})


# Create your views here.
class MyView(APIView):
    # permission_classes = [AuthenticatedOnly]

    def post(self,request):
        print('post')
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

