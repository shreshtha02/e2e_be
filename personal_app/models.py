from django.db import models


# Create your models here.
class React(models.Model):
    name = models.CharField(max_length=30)
    detail = models.CharField(max_length=500)



# from pymongo import Connection
# from pymongo import MongoClient
# databaseName = "e2e_db"
# connection = Connection()
#
# db = connectiondatabaseNameemployees = db'personal_users'
# person1 = { "user_name" : "John.Doe",
#             "first_name" : "John", "last_name": "Doe", "mobile":3829038,"unique_id":2352352 }
#
# person2 = { "user_name" : "Avy.Doe",
#             "first_name" : "Avy", "last_name":"Doe","mobile":3829038,"unique_id":8749873489 }
#
# print("clearing")
# employees.remove()
#
# print("saving")
# employees.save(person1)
# employees.save(person2)
#
# print "searching"
# for e in employees.find():
#     print e["name"] + " " + unicode(e["languages"])