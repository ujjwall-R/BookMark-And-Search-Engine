from settings import *
import requests
from requests.exceptions import RequestException
import pandas as pd
from storage import DBStorage
from datetime import datetime
from urllib.parse import quote_plus


def search_api(query, pages=int(RESULT_COUNT/10)):
    results = []
    for i in range(0, pages):
        start = i*10+1
        url = SEARCH_URL.format(
            key=SEARCH_KEY,
            cx=SEARCH_ID,
            query=quote_plus(query),
            start=start
        )
        response = requests.get(url)
        data = response.json()
        if (data['searchInformation']['totalResults']) == '0':
            continue
        results += data["items"]
    res_df = pd.DataFrame.from_dict(results)
    if (len(results) == 0):
        return res_df
    res_df["rank"] = list(range(1, res_df.shape[0] + 1))
    res_df = res_df[["link", "rank", "snippet", "title"]]
    return res_df


def scrape_page(links):
    html = []
    for link in links:
        try:
            data = requests.get(url=link, timeout=5).text
            # print("DATA :", data)
            html.append(data)
        except RequestException:
            html.append("")
    return html


def search(query):
    columns = ["query", "rank", "link", "title", "snippet", "html", "created"]
    storage = DBStorage()

    stored_results = storage.query_results(query)
    stored_recommendation = storage.query_recommendations(query)
    if stored_results.shape[0] > 0:
        print("Searched result already in database!")
        stored_results["created"] = pd.to_datetime(stored_results["created"])
        if stored_recommendation.shape[0] == 0:
            storage.insert_row_recommendations(query)
            print('Query added to database for recommendation.')
        else:
            print('Query already in recommendation database.')
        return stored_results[columns]

    print("No results in database.  Using the API.")
    results = search_api(query)
    if (len(results) == 0):
        return results
    html = scrape_page(results["link"])
    results["html"] = html
    results = results[results["html"].str.len() > 0].copy()
    results["query"] = query
    results["created"] = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
    results = results[columns]
    results.apply(lambda x: storage.insert_row(x), axis=1)
    print(f"Inserted {results.shape[0]} records.")
    return results


def get_all_recommendations():
    storage = DBStorage()
    AllRecommendations = storage.all_recommendations()
    recommendations = []
    for index, row in AllRecommendations.iterrows():
        recommendations.append(row['query'])
    return recommendations
