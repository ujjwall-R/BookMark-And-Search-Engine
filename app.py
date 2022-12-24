from flask import Flask, request, jsonify
from search import search
from search import get_all_recommendations
from storage import DBStorage
import html
from settings import *
import requests
from requests.exceptions import RequestException
import pandas as pd
from storage import DBStorage
from datetime import datetime
from urllib.parse import quote_plus

languages = ["C++", "Python", "PHP", "Java", "C", "Ruby",
             "R", "C#", "Dart", "Fortran", "Pascal", "Javascript"]

app = Flask(__name__)

styles = """
<style>
    .site {
        font-size: .8rem;
        color: green;
    }

    .snippet {
        font-size: .9rem;
        color: gray;
        margin-bottom: 30px;
    }
</style>
"""

search_template = """"""

result_template = """
<p class="site">{rank}: {link}</p>
<a href="{link}">{title}</a>
<p class="snippet">{snippet}</p>
"""

cannot_search_empty_form_template = """<p>Please Enter query to search!!</p>"""
no_results_found_template = """<p>No result found!!<p>"""


def show_search_form(page=""""""):
    recommendation = get_all_recommendations()
    script_ = """<script>
            $( function() {
            var availableTags = ["""
    for query in recommendation:
        script_ = script_ + f""" "{query}","""
    script_ = script_ + """];

            $( "#query" ).autocomplete({
            source: availableTags
            });
        } );
    </script>"""
    script_ = """<head>
    <title>BookMark</title>
    <script src="https://ajax.googleapis.com/ajax/libs/jquery/1.7.1/jquery.js">  
    </script>  
    
    <script src="https://ajax.googleapis.com/ajax/libs/jqueryui/1.8.16/jquery-ui.js">  
    </script>  
    
    <link href="http://ajax.googleapis.com/ajax/libs/jqueryui/1.8.16/themes/ui-lightness/jquery-ui.css"
        rel="stylesheet" type="text/css" />  
    </head>
    <body>
     <form action="/" method="post">
      <input type="text" name="query" id="query">"""+script_+"""<input type="submit" value="Search">
    </form>
    </body>"""
    return styles+script_+page


def run_search(query):
    results = search(query)
    rendered = """"""
    try:
        results["snippet"] = results["snippet"].apply(lambda x: html.escape(x))
    except KeyError as error:
        return show_search_form(no_results_found_template)

    for index, row in results.iterrows():
        rendered += result_template.format(**row)
    return show_search_form(rendered)


@ app.route("/", methods=['GET', 'POST'])
def search_form():
    if request.method == 'POST':
        query = request.form["query"]
        if len(query) == 0:
            return show_search_form(cannot_search_empty_form_template)
        return run_search(query)
    else:
        return show_search_form()
