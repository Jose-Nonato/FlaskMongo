from this import d
from flask import Flask, Response, request
import pymongo
import json
from bson.objectid import ObjectId

app = Flask(__name__)

try:
    mongo = pymongo.MongoClient("mongodb://localhost:27017/")
    db = mongo.company
    mongo.server_info()
except:
    print("ERROR -Cannot connect to DB")

##############################Update Operation#################################

@app.route("/users/<id>", methods=["PATCH"])
def update_user(id):
    try:
        dbResponse = db.users.update_one(
            {"_id": ObjectId(id)},
            {"$set": {"name": request.form["name"]}}
        )
        if dbResponse.modified_count == 1:
            return Response(
                response=json.dumps({"message": "user updated"}),
                status=200,
                mimetype="application/json"
            )
        else:
            return Response(
                response=json.dumps({"message": "nothing to update"}),
                status=200,
                mimetype="application/json"
            )
    except Exception as ex:
        print("*"*10)
        print(ex)
        print("*"*10)
        return Response(
            response=json.dumps({"message": "sorry cannot update user"}),
            status=500,
            mimetype="application/json"
        )

##############################Read Operation#################################

@app.route("/users", methods=["GET"])
def get_user():
    try:
        data = list(db.users.find())
        for user in data:
            user["_id"] = str(user["_id"])
        return Response(
            response=json.dumps(data),
            status=500,
            mimetype="application/json"
        )
    except Exception as ex:
        return Response(
            response=json.dumps({"message": "cannot read user"}),
            status=500,
            mimetype="application/json"
        )

##############################Create Operation################################

@app.route("/users", methods=["POST"])
def create_user():
    try:
        user = {
            "name": request.form["name"], 
            "lastName": request.form["lastName"]
        }
        dbResponse = db.users.insert_one(user)
        print(dbResponse)
        return Response(
            response=json.dumps({"message": "user created", "id": f"{dbResponse.inserted_id}"}),
            status=200,
            mimetype="application/json"
        )
    except Exception as ex:
        return ex

###############################################################

if __name__ == "__main__":
    app.run(port=80, debug=True)