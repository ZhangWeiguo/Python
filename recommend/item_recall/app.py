# -*- encoding:utf-8 -*-
# created by zwg WegoZng in 20180501
from flask import Flask,request
from flask.views import MethodView
# from recall_model import RecallModel
from model_pai_swing import SwingPai as RecallModel
import json

def index():
    return "App Is Running"

def similar():
    video_id = request.values.get("video_id")
    data = {"msg":"","status":"succ","video_id":"","similars":[]}
    if video_id:
        data["video_id"] = video_id
        similars = model.recall(video_id)
        data["similars"] = similars
    else:
        data["msg"] = "video_id is required"
        data["status"] = "error"
    return json.dumps(data)



if __name__ == "__main__":
    video_filename = "videos.csv"
    rec_filename = "rec.csv"
    model = RecallModel(rec_filename, video_filename)
    app = Flask(__name__)
    app.add_url_rule('/',          view_func=index)
    app.add_url_rule('/similar',   view_func=similar)
    app.run()