
from datetime import datetime
from smartnews import db
from smartnews.models import NewsSources, NewsFeeds, NewsTags, NewsTagPivot
from sqlalchemy.exc import IntegrityError


class NewsFeedService:
    def __init__(self):
        pass

    def save_news_feeds(self, news_feed, country):
          # check if we previously had a news with feeds by title
        news_feed_exist = self.news_feed_exist_by_name(news_feed)
        if news_feed_exist:
            return ""
        # News feed is a new one, save it and its details in the db
        # set the country as property on the news feed distionary
        news_feed['country'] = country
        post_news_feed = self.generateNewsFeed(news_feed)
        news_feed_status = 0
        # save the news feed main data into db
        try:
            db.session.add(post_news_feed)
            db.session.commit()
            # Increment counter to indicate we have inserted a new data successfully
            news_feed_status += 1
        except IntegrityError:
            db.session.rollback()
            print(
                'Duplicate entry detected, rollback status of database to ignore the exception')

        # save the created news feed and its associated tags
        if news_feed_status > 0:
            self.save_news_tags_pivot(
                post_news_feed.id, news_feed['post_tags'])
            return "saved"
        else:
            return "Not Saved"

    def generateNewsFeed(self, news_feed):

        post_news_feed = NewsFeeds()
        post_news_feed.post_title = news_feed['post_title'].strip()
        post_news_feed.post_image_url = news_feed['post_image']
        post_news_feed.post_summary = news_feed['post_summary']
        post_news_feed.post_url = news_feed['post_url']
        post_news_feed.post_source_id = self.get_news_source_id_by_name(
            news_feed)  # Find news_feed source by id
        post_news_feed.post_country_id = news_feed['country']
        post_news_feed.post_date = news_feed['post_date']
        post_news_feed.created_at = datetime.now()

        return post_news_feed

    def save_news_tags_pivot(self, news_id, news_tags):
        news_id = news_id
        # save all current news_feed tags to db and retun their ids
        news_tags_id = self.save_news_feed_tags(news_tags)
        # Loop through list ids and save in pivot table for
        for tag_id in news_tags_id:
            # create a news_tag_pivot row to track news feed and tags table
            news_tags_pivot = NewsTagPivot(
                news_id=news_id, tag_id=tag_id, created_at=datetime.now())
            db.session.add(news_tags_pivot)
        # commit all tags pivot to db pivot table
        db.session.commit()

    # check if a news feed about to be saved exist already by
    def news_feed_exist_by_name(self, news_feed):
        post_title = news_feed['post_title'].strip()
        post_date = news_feed['post_date']
        feeds_exist = False
        news_feed_exist = NewsFeeds.query.filter_by(
            post_title=post_title, post_date=post_date).first()
        if news_feed_exist is not None:
            feeds_exist = True
        return feeds_exist

    def get_news_source_id_by_name(self, news_feed):
        # get news source by name if exist, if not, create a new one and return id
        source_name = news_feed['post_source_name'].strip()
        source_logo = news_feed['post_source_logo'].strip()
        source_exist = NewsSources.query.filter_by(logo=source_logo).first()
        if source_exist is not None:
            return source_exist.id
        # create a new source and return id
        return self.save_news_feed_source(source_name, source_logo)

    def save_news_feed_source(self, source_name, source_logo):
        news_feed_source = NewsSources(
            name=source_name, logo=source_logo, domain='', created_at=datetime.now())
        db.session.add(news_feed_source)
        db.session.commit()
        return news_feed_source.id

    def get_news_tag_id_by_name(self, tag):
        tag_id = 0
        tag_exist = NewsTags.query.filter_by(name=tag).first()
        if tag_exist is not None:
            tag_id = tag_exist.id
        return tag_id

    def save_news_feed_tags(self, news_tags):
         # Save list of tags  and retun ids
        tag_list_ids = []
        for tag in news_tags:
            # check if tag exist, return it or create a new one
            tag_exist_id = self.get_news_tag_id_by_name(tag)
            if tag_exist_id > 0:
                tag_list_ids.append(tag_exist_id)
            else:
                # create a new tag and return its id instead, doesn't exist
                new_tag = NewsTags(name=tag, created_at=datetime.now())
                db.session.add(new_tag)
                db.session.commit()
                tag_list_ids.append(new_tag.id)

        return tag_list_ids
