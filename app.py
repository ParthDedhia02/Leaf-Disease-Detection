import numpy as np
from flask import Flask,jsonify,request,render_template
import pickle

app=Flask(__name__)

model=pickle.load(open("model.pkl","rb"))

@app.route("/")
def Home():
    return render_template("index.html")


@app.route("/predict",method=["POST"])
def predict
