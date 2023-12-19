import os
from pyspark.sql import SparkSession
from pyspark.sql.types import StructType, StructField, StringType, FloatType
from database import get_database_url, get_session, create_news

PATH_TO_DATA = "/app/news_collector/data"

spark = SparkSession.builder.appName("news_collector").getOrCreate()

database_url = get_database_url(db_host=os.environ["DB_HOSTNAME"],
                                db_user=os.environ["DB_USER"],
                                db_pass=os.environ["DB_USER_PASSWORD"])


def func(df, batch_id):
    """

    :param df:
    :param batch_id:
    :return:
    """
    news = []
    for row in df.toLocalIterator():
        data = {
            "news_id": row.id,
            "url": row.url,
            "title": row.title,
            "datetime": row.datetime,
            "author": row.author,
            "news_text": row.text,
            "provider": row.provider,
            "source": row.source,
            "pro_israel_score": row.pro_israel_score
        }
        news.append(data)

    Session = get_session(database_url)

    create_news(Session, news)


news_schema = StructType([
    StructField('id', StringType()),
    StructField('url', StringType()),
    StructField('title', StringType()),
    StructField('datetime', StringType()),
    StructField('author', StringType()),
    StructField('text', StringType()),
    StructField('provider', StringType()),
    StructField('source', StringType()),
    StructField('pro_israel_score', FloatType()),
])
news = spark.readStream.schema(news_schema).csv(PATH_TO_DATA, header=True, sep=';')

query = news.writeStream.foreachBatch(func).trigger(processingTime='1 hour').start()
query.awaitTermination()
