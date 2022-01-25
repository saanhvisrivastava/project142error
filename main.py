from flask import Flask, jsonify, request
import csv
from demographic_filtering import output
from content_filtering import get_recommendations

all_articles = []

with open('articles.csv',encoding='utf-8') as f:
    reader=csv.reader(f)
    
    data = list(reader)
    all_articles = data[1:]

liked_article = []
not_liked_article = []
did_not_read = []

app = Flask(__name__)

@app.route("/get-article")
def get_article():
    global all_articles
    return jsonify({
        "data": all_articles[0],
        "status": "success"
    })

@app.route("/liked-article", methods=["POST"])
def liked_article():
    global all_articles
    article = all_articles[0]
    all_articles = all_articles[1:]
    liked_article.append(article)
    return jsonify({
        "status": "success"
    }), 201

@app.route("/unliked-article", methods=["POST"])
def unliked_article():
    global all_articles
    article = all_articles[0]
    all_articles = all_articles[1:]
    not_liked_article.append(article)
    return jsonify({
        "status": "success"
    }), 201

@app.route("/did-not-read", methods=["POST"])
def did_not_read():
    global all_articles
    article = all_articles[0]
    all_articles = all_articles[1:]
    did_not_read.append(article)
    return jsonify({
        "status": "success"
    }), 201



@app.route("/popular-articles",methods=["POST"])
def popular_articles():
    article_data = []#timestamp,eventType,contentId,personId,sessionId
    for article in output:
        _d = {
            "timestamp": article[0],
            "eventType": article[1],
            "contentId": article[2] or "N/A",
            "personId": article[3],
            "sessionId": article[4],
           
        }
        article_data.append(_d)
    return jsonify({
        "data": article_data,
        "status": "success"
    }), 200

@app.route("/recommended-articles",methods=["POST"])
def recommended_articles():
    all_recommended = []
    for liked_article in liked_article :
        output = get_recommendations(liked_article[19])
        for data in output:
            all_recommended.append(data)
    import itertools
    all_recommended.sort()
    all_recommended = list(all_recommended for all_recommended,_ in itertools.groupby(all_recommended))
    article_data = []
    for recommended in all_recommended:
        _d = {
            "timestamp": recommended[0],
            "eventType": recommended[1],
            "contentId": recommended[2] or "N/A",
            "personId": recommended[3],
            "sessionId": recommended[4],
           
        }
        article_data.append(_d)
    return jsonify({
        "data": article_data,
        "status": "success"
    }), 200




if __name__ == "__main__":
  app.run()