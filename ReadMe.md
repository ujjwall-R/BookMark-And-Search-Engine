# Introduction

Goal is to have a good search experience when searching through the given JSON
file [(link)](https://drive.google.com/file/d/1vDhDMA_HiUWz7t9xSVAZ82tZPYJTKqvt/view?usp=sh%20aring). The file contains the links saved by a user on a daily basis,
this includes articles which are saved for reference or for future reading.

# Preparation

## Build Custom Search Engine

The main objective we have is creation of a custom search engine which search among the available set of links/websites. One of the approach we could have used is maybe using open source search engine like MilieSearch. But, since the websites in the JSON file may be completely random(some are blog site, some maybe just a link to a product of ecommerce site etc), it is very difficult to crawl or get an indexed dataset to search on.

### Google programmable search engine

Google provides a service where we can setup a [programmable search engine](https://programmablesearchengine.google.com/about/) where we can customize the search engine in a smart manner.

Refer this 3 minute [youtube video](https://www.youtube.com/watch?v=7avwo2xrbwY) to setup the engine.

Now the challenge we have is to add the custom domains one by one or all together together in a manner that the links are in new line.

```bash
cd "cse preparer"
npm i
node app
```

Now we will have all the links in seperated lines in links.txt file in the same directory. app.js extracts the links from json and add into .txt file so that we can use it directly into the cse service by google bot.

Copy everything in the links.txt file and move to the control panel of your custom search engine and under sites to search add paste everything inside it.
![adding of link snapshot](https://github.com/ujjwall-R/BookMark-And-Search-Engine/blob/master/cse%20preparer/images/Screenshot%20from%202022-12-25%2010-25-23.png?raw=true)
Save to Continue.

Congratulations! You already have a working search engine that works the same intended way.

![Working search engine](https://github.com/ujjwall-R/BookMark-And-Search-Engine/blob/master/cse%20preparer/images/Screenshot%20from%202022-12-25%2010-17-09.png?raw=true)

To enhance user experience, we will use a flask application and sqlite database and use google cse api to fetch the search results.

## Setting up the flask application

I have made a flask application that uses the google custom search engine api and finds the result.

### Benefits of building the app and not using the google search bar

- In case of any successful search, we store the query and result in the database. This makes the app fast in case of further similar search. Also, we can create a custom filtering and ranking using any machine learning techniques later on in our project.
- I built a recommendation system. So in case of every successful search, the query is stored in the database in another table of recommendations. I am currently using [jQuery Autocomplete](https://jqueryui.com/autocomplete/) to implement the feature.
- In short, the more the search engine is used, the better will be our recommendation system be. It is analogous to training the model after successful search. This ensures that only correct and relevant recommendations are provided. No such recommendation is shown which results in no search result.

- When there is a successful search, if there is no such query in the recommendations database, the query is stored for the betterment of recommendations for other users or future searches

- Another benefit of using flask app is that I can play with the UI as per my wish. Its always more handy.

# Usage

Move to the root directory of the project
Open settings.py
You will see the following:

```python
SEARCH_KEY = ""
SEARCH_ID = ""

SEARCH_URL = "https://www.googleapis.com/customsearch/v1?key={key}&cx={cx}&q={query}&start={start}&num=10&gl="
RESULT_COUNT = 10

```

Get the search engine ID from the control panel of your custom search engine and add into SEARCH_ID. Also, get the API key and add into SEARCH_KEY.

#### For evaluation [Temporary section]

You need not to create your own custom search engine (preparation steps) if you use my key and id. These are my key and api id. I will soon remove this from the repository. Its only for evaluation purpose(as Google API only gives first free 10000 searches per day).

```python
SEARCH_KEY = "AIzaSyD6_svwnad4NrzQ7DBTyGiUxzcy_1VJ3Bc"
SEARCH_ID = "94ed76e4186f6414f"
```

Install requirements.

```bash
pip install requirements.txt
```

'or'

```bash
pip install flask pandas requests beautifulsoup4
```

Start the application.

```bash
flask --debug run --port 5001
```

Open the link of the deployed port and you can use the application. In this case it is

```website
http://127.0.0.1:5001/
```

## Contributing

Pull requests are welcome. For major changes, please open an issue first
to discuss what you would like to change.

### License

[MIT](https://choosealicense.com/licenses/mit/)
