# Launch with
#
# gunicorn -D --threads 4 -b 0.0.0.0:5000 --access-logfile server.log --timeout 60 server:app glove.6B.300d.txt bbc

from flask import Flask, render_template
from doc2vec import *
import sys

app = Flask(__name__)


@app.route("/")
def articles():
    """Show a list of article titles"""
    tup_list = []
    for record in articles:
        filename = record[0]
        path = '/article/' + filename
        title = record[1]
        tup = (path, title)
        tup_list.append(tup)

    return render_template('articles.html', tup_list=tup_list)


@app.route("/article/<topic>/<filename>")
def article(topic, filename):
    """
    Show an article with relative path filename. Assumes the BBC structure of
    topic/filename.txt so our URLs follow that.
    """
    filename = topic + '/' + filename
    n_articles = None
    for article in articles:
        if article[0] == filename:
            title = article[1]
            cond = article[2]
            n_articles = recommended(article, articles, 5)
            break

    tup_list = []
    for record in n_articles:
        filename = record[0]
        path = '/article/' + filename
        t = record[1]
        tup = (path, t)
        tup_list.append(tup)

    return render_template('article.html', title=title, cond=cond, tup_list=tup_list)


# initialization
i = sys.argv.index('server:app')
glove_filename = sys.argv[i+1]
articles_dirname = sys.argv[i+2]

# glove_filename = sys.argv[1]
# articles_dirname = sys.argv[2]

gloves = load_glove(glove_filename)
articles = load_articles(articles_dirname, gloves)

# app.run()
