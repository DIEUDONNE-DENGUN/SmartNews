
def format_news_date(news_feed_date):
    # remove T and Z from news_feed date
    publish_date = news_feed_date.strip()
    publish_date = publish_date.replace("Z", "")
    publish_date = publish_date.replace("T", " ")
    return publish_date

# Strip news field text field and set defualt value to empty string if not set
def format_news_field_field(news_feed_field):
    field = news_feed_field if news_feed_field is not None else ""
    news_feed_field = field.strip()
    return news_feed_field
