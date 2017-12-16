from flask import Flask, render_template, url_for, json
import os,pdb
import sys
sys.path.insert(0,'/home/lptprgmain/Desktop/ArticleBits')
from mysqlconnection import connection
from testing import testingresult

app = Flask(__name__)

@app.route('/')
def index():
  return render_template('index.html')

@app.route('/dashboard')
def dashboard():
  return render_template('dashboard.html')

@app.route('/sitelogic')
def sitelogic():
    return render_template('sitelogic.html')

@app.route('/developernotes')
def developernotes():
    return render_template('developernotes.html')

@app.route('/<category>')
def infopage(category):
    SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
    json_url = os.path.join(SITE_ROOT, "static/data", "res.json")
    data = json.load(open(json_url))
    catdict = {'topstories':'Top Stories','world':'World','us':'US','politics':'Politics','technology':'Technology','health':'Health','business':'Business','science':'Science','asia':'Asia','europe':'Europe','middleeast':'Middle East','finance':'Finance','lifestyle':'Lifestyle'}
    category_formatted = catdict[category]
    env = data[category_formatted]
    companies = list(env.keys())
    return render_template('infopage.html',env=env,companies=companies,category=category)

@app.route('/<category>/<articleid>')
def infopagearticle(category,articleid):
    SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
    json_url = os.path.join(SITE_ROOT, "static/data", "res.json")
    data = json.load(open(json_url))
    catdict = {'topstories':'Top Stories','world':'World','us':'US','politics':'Politics','technology':'Technology','health':'Health','business':'Business','science':'Science','asia':'Asia','europe':'Europe','middleeast':'Middle East','finance':'Finance','lifestyle':'Lifestyle'}
    category_formatted = catdict[category]
    env = data[category_formatted]
    companies = list(env.keys())
    with connection.cursor() as cursor:
        sql_string = "SELECT * FROM NewsStoriesProduction WHERE Category = '{}' and Id = '{}'".format(category_formatted,articleid)
        cursor.execute(sql_string)
        results = cursor.fetchall()[0]

    terms = results['Terms']
    try:
        term_set_split = [i.split('::') for i in terms.split('|:|')]
        unpack_terms = {s[0]:s[1] for s in term_set_split}
    except:
        unpack_terms = {'None':'No Matched Terms'}

    
    grouped_titles = [results['MatchedID_1'],results['MatchedID_2'],results['MatchedID_3'],results['MatchedID_4'],results['MatchedID_5']]
    if len(grouped_titles) > 1: 
        matched_titles = []
        for grouped_title in grouped_titles:
            for category_search in data.keys():
                for company in data[category_search].keys():
                    if grouped_title in data[category_search][company].keys() and category_search != category_formatted:
                        matched_titles.append([grouped_title,company,category_search.lower().replace(' ',''),data[category_search][company][grouped_title]])
            
        # formatted_matched_titles = list(set(matched_titles))
        formatted_matched_titles = matched_titles
    else:
        formatted_matched_titles = []
    
    return render_template('infopagearticle.html',env=env,companies=companies,category=category,articleresults=results,terms=unpack_terms,grouped=formatted_matched_titles)
    
if __name__ == '__main__':
  app.run(debug=True)
