from datetime import datetime

"""
    Wrap the date from the api, and send the list of news obj to frontend
"""

class News_List:
    """news list wrapper class"""

    def __init__(self):
        self.list = []

    def news_mapper(self, res):
        """map the each news to news_obj and append to the list"""
        articles = res['articles']
        for news in articles:
            desc = str(news['description'])
            if(len(desc)>150):
                desc = desc[0:150] + "..."
            
            news_obj = News_Obj(
                news['url'], news['title'], desc, news['publishedAt'], news['urlToImage'])
            self.list.append(news_obj)


class News_Obj:
    """news obj wrapper class"""

    def __init__(self, url, title, description, date, image):
        self.url = url
        self.title = title
        self.description = description
        self.date = datetime.strptime(date, "%Y-%m-%dT%H:%M:%S%z")
        self.image = image
