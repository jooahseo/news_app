
class News_List:
    """news list wrapper class"""
    def __init__(self):
        self.list = []
    

    def news_mapper(self,res):
        """map the each news to news_obj and append to the list"""
        articles = res['articles']
        print ("********** How articles look like? ***********")
        print(articles)
        for news in articles:
            news_obj = News_Obj(news['url'], news['title'], news['description'], news['publishedAt'], news['urlToImage'])
            self.list.append(news_obj)


class News_Obj:
    """news obj wrapper class"""
    def __init__(self,url,title,description,date,image):
        self.url = url
        self.title = title
        self.description = description
        self.date = date
        self.image = image
