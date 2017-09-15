# Reddit Crawler

You have to create config.ini file with the following structure:

[REDDIT]
ClientID: your reddit id
ClientSecret: your reddit secret

[IMGUR]
ClientID: your imgur id
ClientSecret: your imgur secret



By default, the subreddit to crawl is 'earthporn' and the number of posts to search  in is 10. You can execute with inline parameters to change this i.e.:
python RedditCrawler.py 50 cactus



To prevent from saving an image twice, a hash is calculated and stored into a .txt file.
