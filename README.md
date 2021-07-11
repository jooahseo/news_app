# news_app

###This is the web application that users can search, save news to their save page. This app is built using Python & JavaScript with data from NewsAPI [https://newsapi.org/](https://newsapi.org/). App is tested with Python’s unittest. 

###App features:
- **For global user (not signed in)**
	- Check today’s top headline
	- Search news

- **For signed in user**
	- Select interest (category) upon signup or on its profile page. 
	- Check recommended news based on the interested category
	- Save news 
	- Check / remove saved news 
	- Delete account

###Screenshot of the app:
On the main page, news will be displayed in the carousel. <br>

**User not signed in**

![Main page before signed in](image/mainpage_global.png?raw=true "Main page before signed in")

**User signed in**

![Main page after signed in](image/mainpage_signedin.png?raw=true "Main page after signed in")

**Searched news “tesla” and the result is being displayed.**
![Search news page](image/search_page.png?raw=true "Search news page")

**User's save page**
![User's save s page](image/save_page.png?raw=true "User's save s page")

#### Technology Used:
- Python
- Flask
- JavaScript
- Bootstrap
- Axios
- Sqlalchemy 
- WTForms
