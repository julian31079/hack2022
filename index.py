from cProfile import label
from flask import Flask,jsonify,send_file
from flask_pymongo import ObjectId,PyMongo,request
from flask_cors import CORS
import datetime
import numpy as np
import matplotlib.pyplot as plt
app = Flask(__name__)
app.config['MONGO_URI']='mongodb://localhost/local'
CORS(app)
mongo=PyMongo(app)
collection=mongo.db.hosp

def calcPercentage(ls):
    sum=0
    for j in ls:
        sum+=(j/len(ls))/5
    return sum
def makeProb(listNutricional,listAfectivo,listFuncional,id):
    date = datetime.datetime.now().strftime("%d-%m-%Y")
    valueArray=np.array([1,2,3,4,5])
    converterNutri= [valueArray[-i] for i in listNutricional]
    converterAfect= [valueArray[-i] for i in listAfectivo]
    converterFunc= [valueArray[-i] for i in listFuncional]
    return {"id":id,"Nutritional":[{"date":date,"value":calcPercentage(converterNutri)}],"Affect":[{"date":date,"value":calcPercentage(converterAfect)}],"Func":[{"date":date,"value":calcPercentage(converterFunc)}]}
def addOne(req):
    old=collection.find_one({"id":req["id"]})
    if(old is None):
        collection.insert_one(req)
    else:
        old["Nutritional"].append(req["Nutritional"][0])
        old["Affect"].append(req["Affect"][0])
        old["Func"].append(req["Func"][0])
        collection.update_one({"id":req["id"]},{"$set":{"Nutritional":old["Nutritional"],"Affect":old["Affect"],"Func":old["Func"]}})

@app.route('/createSt',methods=['POST'])
def createStory():
    addOne(makeProb(request.json["listNutricional"],request.json["listAfectivo"],request.json["listFunc"],request.json["id"]))
    return jsonify({'msg':'created'})
@app.route('/getGraphN/<string:id>',methods=['GET'])
def graph(id):
    print(id)
    data=collection.find_one({"id":id})
    date=[d["date"] for d in data["Nutritional"]]
    value=[d["value"] for d in data["Nutritional"]]
    plt.plot(date,value)
    plt.ylabel("Probabilidad de riesgo")
    plt.xlabel("Tiempo")
    plt.savefig("imgN.png")
    return send_file("imgN.png",mimetype="image/png")
@app.route('/getGraphA/<string:id>',methods=['GET'])
def graph1(id):
    print(id)
    data=collection.find_one({"id":id})
    date=[d["date"] for d in data["Affect"]]
    value=[d["value"] for d in data["Affect"]]
    plt.plot(date,value)
    plt.ylabel("Probabilidad de riesgo")
    plt.xlabel("Tiempo")
    plt.savefig("imgA.png")
    return send_file("imgA.png",mimetype="image/png")
@app.route('/getGraphF/<string:id>',methods=['GET'])
def graph2(id):
    print(id)
    data=collection.find_one({"id":id})
    date=[d["date"] for d in data["Func"]]
    value=[d["value"] for d in data["Func"]]
    plt.plot(date,value)
    plt.ylabel("Probabilidad de riesgo")
    plt.xlabel("Tiempo")
    plt.savefig("imgF.png")
    return send_file("imgF.png",mimetype="image/png")
@app.route('/pronostic/<string:id>',methods=['GET'])
def pronostic(id):
    data=collection.find_one({"id":id})
    date=[d["date"] for d in data["Nutritional"]]
    value=[d["value"] for d in data["Nutritional"]]
    plt.plot(date,value,"red",label="Real")
    testDatax=["14-10-2022","15-10-2022","16-10-2022"]
    testDatay=[0.3,0.2,0.5]
    plt.plot(testDatax,testDatay,"blue",label="Pronostico")
    plt.ylabel("Probabilidad de riesgo")
    plt.xlabel("Tiempo pronostico")
    plt.legend()
    plt.savefig("imgF.png")
    return send_file("imgF.png",mimetype="image/png")

if __name__ == "__main__":
    app.run(debug=True)

    #app.debug=True
    #app.run(host="192.168.20.25")
