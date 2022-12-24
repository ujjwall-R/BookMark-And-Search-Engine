from flask import Flask, request, jsonify
from search import search
from storage import DBStorage
import html

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

    .rel-button {
        cursor: pointer;
        color: blue;
    }
</style>
<script>
const relevant = function(query, link){
    fetch("/relevant", {
        method: 'POST',
        headers: {
          'Accept': 'application/json',
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
           "query": query,
           "link": link
          })
        });
}
</script>
"""

search_template = styles + """
     <form action="/" method="post">
      <input type="text" name="query">
      <input type="submit" value="Search">
    </form>
    """

result_template = """
<p class="site">{rank}: {link}</p>
<a href="{link}">{title}</a>
<p class="snippet">{snippet}</p>
"""

cannot_search_empty_form_template = """<p>Please Enter query to search!!</p>"""
no_results_found_template = """<p>No result found!!<p>"""


def show_search_form():
    return search_template


def run_search(query):
    results = search(query)
    rendered = search_template
    try:
        results["snippet"] = results["snippet"].apply(lambda x: html.escape(x))
    except KeyError as error:
        return rendered + no_results_found_template

    for index, row in results.iterrows():
        rendered += result_template.format(**row)
    return rendered


@ app.route("/", methods=['GET', 'POST'])
def search_form():
    if request.method == 'POST':
        query = request.form["query"]
        if len(query) == 0:
            return search_template+cannot_search_empty_form_template
        return run_search(query)
    else:
        return show_search_form()
