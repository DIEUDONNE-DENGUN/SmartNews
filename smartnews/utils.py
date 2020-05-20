
def format_news_date(news_feed_date):
    # remove T and Z from news_feed date
    publish_date = news_feed_date.strip()
    publish_date = publish_date.replace("Z", "")
    publish_date = publish_date.replace("T", " ")
    return publish_date
