from flask import Flask, render_template
import pymongo

app = Flask(__name__)

try:
    mydb = pymongo.MongoClient("mongodb://localhost:27017/")
    db = mydb["CrudFlask"]
    print("Conectado")
except:
    print("Tente novamente")

@app.route("/")
def Initial():
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)