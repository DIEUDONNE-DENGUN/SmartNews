import requests
from bs4 import BeautifulSoup
import csv


class WebCrawler:
    def __init__(self):
        self.base_url = 'http://237dailynews.com/'
        self.daily_news_container = ''
        self.daily_news_json_list = []
        self.top_headlines_container = ''
        self.popular_news_container = ''
        # self.initialize_beautiful_soup()

    def initialize_beautiful_soup(self):
        #  set up request
        web_request = requests.get(self.base_url)
        beautiful_soup_instance = BeautifulSoup(
            web_request.content, 'html5lib')
        self.daily_news_container = beautiful_soup_instance.find_all(
            'div', class_='row')
        self.top_headlines_container = self.daily_news_container[1]
        self.popular_news_container = self.daily_news_container[3]
        # reset news post list everytime initialized
        self.daily_news_json_list = []

    def extract_top_news_headlines(self):
        # Get all top headlines or recent news (col-md-4 of first news row)
        latest_news = self.top_headlines_container.find(
            'div', class_='col-md-4')
        latest_news_containers = latest_news.find_all(
            'div', class_='container')
        # Loop through headlines and get all news content
        for headline_container in latest_news_containers:
            headline_title = headline_container.find('h3').text
            headline_url = self.base_url + headline_container.select(
                'a[href^="posts?p"]')[1]['href']
            post_tags = headline_container.select(
                'span[style^="color: white; background-color: #DC3545;margin: 2px"]')
            headline_tags_container = []
            for post_tag in post_tags:
                post_tag_title = post_tag.select_one(
                    'span[style="color: white;padding: 2px"]').text
                headline_tags_container.append(post_tag_title)

            headline_feature_img = headline_container.find(
                'img', class_='img-fluid')['src']
            headline_source_logo = headline_container.select_one(
                'img[style="width: 50px; height: 40px; float: left"]')['src']
            headline_source_name = headline_container.select('a[href^="posts?p"]')[
                1].text
            headline_publish_date = headline_container.find(
                'span', class_='pubDate').text
            headline_publish_timezone = headline_container.find(
                'span', 'pubTimezone').text
            headline_summary_text = headline_container.find(
                'p', class_='card-text').text
            headline_post = {
                "post_title": headline_title,
                "post_image": headline_feature_img,
                "post_url": headline_url,
                "post_source_name": headline_source_name,
                "post_source_logo": headline_source_logo,
                "post_summary": headline_summary_text,
                "post_tags": headline_tags_container,
                "post_date": headline_publish_date,
                "post_timezone": headline_publish_timezone,
            }
            # Add top news headlines to the daily news json list
            self.daily_news_json_list.append(headline_post)

    def build_trending_news(self):
        # get all trending news after headlines
        trending_news = self.top_headlines_container.find(
            'div', class_='col-md-8')
        trending_news_row = trending_news.find('div', class_='row')
        trending_news_containers = trending_news_row.find_all(
            'div', 'col-md-4')
        # extract and build the trending news and store in list
        self.extract_build_news_posts_trending(
            trending_news_containers)

    def extract_build_news_posts_trending(self, posts):
        # extract and build trending news (col-md-8 of first news row)
        for post in posts:
            post_title = post.select_one(
                'a[style^="font-style: italic; text-decoration: none;color: #1e2023"]').find('b').text
            post_url = self.base_url + post.select_one(
                'a[style^="font-style: italic; text-decoration: none;color: #1e2023"]')['href']
            post_source_name = post.select('a[href^="posts?p"]')[1].text
            post_feature_img = post.find('img', class_='img-fluid')['src']
            post_source_logo = post.select_one(
                'img[style="width: 50px; height: 40px; float: left"]')['src']
            post_source_name = post.select(
                'a[href^="posts?p"]')[2].text
            post_publish_date = post.find(
                'span', class_='pubDate').text
            post_publish_timezone = post.find(
                'span', 'pubTimezone').text
            post_summary_text = post.find(
                'p', class_='card-text').text
            post_tags = post.select(
                'span[style^="color: white; background-color: #DC3545;margin: 2px"]')
            post_tags_container = []
            for post_tag in post_tags:
                tag_title = post_tag.select_one(
                    'span[style="color: white;padding: 2px"]').text
                post_tags_container.append(tag_title)
            news_post = {}
            news_post = {
                "post_title": post_title,
                "post_image": post_feature_img,
                "post_url": post_url,
                "post_source_name": post_source_name,
                "post_source_logo": post_source_logo,
                "post_summary": post_summary_text,
                "post_tags": post_tags_container,
                "post_date": post_publish_date,
                "post_timezone": post_publish_timezone,
            }
            self.daily_news_json_list.append(news_post)

    def build_posts_popular(self):
        # Get all col-md-3 in the popular news row
        popular_news_containers = self.popular_news_container.find_all(
            'div', 'col-md-3')
        # Extract and store all populars news content into the list of news post
        self.extract_build_news_popular(popular_news_containers)

    def extract_build_news_popular(self, posts):

        for post in posts:
            post_title = post.select_one(
                'a[style="text-decoration: none; color: #1e2023; font-weight: bold; font-size: medium"]').text
            post_url = self.base_url + post.select_one(
                'a[style="text-decoration: none; color: #1e2023; font-weight: bold; font-size: medium"]')['href']
            post_source_name = post.select('a[href^="posts?p"]')[2].text
            post_feature_img = post.find('img', class_='float-left')['src']
            post_source_logo = post.find('img', class_='img-thumbnail')['src']
            post_publish_date = post.find(
                'span', class_='pubDate').text
            post_publish_timezone = post.find(
                'span', 'pubTimezone').text
            post_summary_text = post.find(
                'p', class_='card-text').text
            post_tags = post.select(
                'span[style^="color: white; background-color: #DC3545;margin: 2px"]')
            post_tags_container = []
            for post_tag in post_tags:
                tag_title = post_tag.select_one(
                    'span[style="color: white;padding: 2px"]').text
                post_tags_container.append(tag_title)
            news_post = {}
            news_post = {
                "post_title": post_title,
                "post_image": post_feature_img,
                "post_url": post_url,
                "post_source_name": post_source_name,
                "post_source_logo": post_source_logo,
                "post_summary": post_summary_text,
                "post_tags": post_tags_container,
                "post_date": post_publish_date,
                "post_timezone": post_publish_timezone,
            }
            self.daily_news_json_list.append(news_post)

    def save_daily_news_csv(self, file_name):

        with open(file_name,  'w', newline='') as f:
            w = csv.DictWriter(f, ['post_title', 'post_image', 'post_url', 'post_source_name',
                                   'post_source_logo', 'post_summary', 'post_tags', 'post_date', 'post_timezone'])
            w.writeheader()
            for post in self.daily_news_json_list:
                w.writerow(post)
        print('News Saved!')

    def run_webcrawler_headlines(self):
        self.initialize_beautiful_soup()
        # get all headlines
        self.extract_top_news_headlines()
        # build and extract trending news
        self.build_trending_news()
        # Get and extract popular news
        self.build_posts_popular()
        # save news crawled to csv
        # self.save_daily_news_csv('daily_news_headlines.csv')

    def run_webcrawler_by_source(self, source):

        # change the baseurl to get from a different url
        self.base_url = self.base_url + '?source=' + source
        # print(web_scrapper.base_url)
        self.initialize_beautiful_soup()
        # get all headlines
        self.extract_top_news_headlines()
        # build and extract trending news
        self.build_trending_news()
        # Get and extract popular news
        self.build_posts_popular()
        # save news crawled to csv
        # self.save_daily_news_csv(source + '_news_headlines.csv')

    def get_all_news_scraped(self):
        
        return self.daily_news_json_list
    
     
# run webcrawler class
# web_scrapper = WebCrawler()
# web_scrapper.run_webcrawler_headlines() #news headlines from homepage
# # web_scrapper.run_webcrawler_by_source('mmi') #mimimefo news headlines
# web_scrapper.run_webcrawler_by_source('CNA') #CNA news headlines
