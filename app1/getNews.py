import requests
from app1.models import Posts

def getExistingURLs():
    urls = []
    allEntries = Posts.objects.all().values()
    for entry in allEntries:
        urls.append(entry["link"])

    return urls

def getTopHeadlines(country="us", category="general"):
    apiKey = "8aac93d6a52b4e69b0d1fe72f526afe5"
    url = "https://newsapi.org/v2/top-headlines?apiKey={}&country={}&category={}"

    response = requests.get(url.format(apiKey, country, category)).json() # returns 20 results
    # check if response is good, aka "status" = ok, "totalResults" != 0, and len("articles") != 0
    if response["status"] != "ok" or response["totalResults"] == 0 or len(response["articles"]) == 0:
        print("Error with get request")
        exit()

    return response["articles"] # list of articles

def insertData(posts, category):
    urlList = getExistingURLs()
    for story in posts:
        # check to see if fields are populated
        if (story["source"]["name"] == None or 
            story["title"] == None or 
            story["description"] == None or 
            story["author"] == None or 
            story["publishedAt"] == None or 
            story["urlToImage"] == None or 
            story["url"] == None):
            continue

        # check to see if url is already in the database
        if story["url"] in urlList:
            #posts.remove(story)
            continue

        # insert story into database
        p = Posts(source=story["source"]["name"],
            title=story["title"],
            description=story["description"],
            author=story["author"],
            datetime=story["publishedAt"],
            image=story["urlToImage"],
            likes=0,
            dislikes=0,
            link=story["url"],
            category=category)
        p.save()

    return

def getNews():
    categories = ["sports", "politics", "business"]
    for c in categories:
        topHeadlines = getTopHeadlines(category=c)
        insertData(topHeadlines, c)

    return

getNews()

# def getTopHeadlinesOld():
#     apiKey = "8aac93d6a52b4e69b0d1fe72f526afe5"
#     sources = "the-new-york-times,cnbc,cnn" #,msnbc,espn,abc-news,bbc-news
#     pageSize = 20
#     url = "https://newsapi.org/v2/top-headlines?apiKey={}&sources={}&pageSize={}&page={}"

#     response = requests.get(url.format(apiKey, sources, pageSize, 1)).json() # 1 is first result
#     # check if response is good, aka "status" = ok, "totalResults" != 0, and len("articles") != 0
#     if response["status"] != "ok" or response["totalResults"] == 0 or len(response["articles"]) == 0:
#         print("Error with get request")
#         exit()

#     totalResults = response["totalResults"] # number of results
#     topHeadlines = response["articles"] # list of articles

#     # get the rest of the articles
#     for pageNum in range(2, 1 + math.ceil(totalResults / pageSize)):
#         topHeadlines += requests.get(url.format(apiKey, sources, pageSize, pageNum)).json()["articles"]

#     print(len(topHeadlines), totalResults)

#     # check to see if url is already there
#     urlList = getExistingURLs()
#     for story in topHeadlines:
#         if story["url"] in urlList:
#             print(story)
#             topHeadlines.remove(story)

#     print(len(topHeadlines), totalResults)
    
#     return topHeadlines