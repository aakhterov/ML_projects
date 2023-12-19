import os
from typing import Dict, List
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import sqlalchemy as sa

news_table = sa.table("news",
                      sa.column("id"),
                      sa.column("news_id"),
                      sa.column("url"),
                      sa.column("title"),
                      sa.column("datetime"),
                      sa.column("author"),
                      sa.column("news_text"),
                      sa.column("provider"),
                      sa.column("source"),
                      sa.column("pro_israel_score"),
                      )


def get_database_url(db_host, db_user, db_pass):
    """

    :param db_host:
    :param db_user:
    :param db_pass:
    :return:
    """
    return f"postgresql+psycopg2://{db_user}:{db_pass}@{db_host}:5432/news"


def get_session(database_url):
    """

    :param database_url:
    :return:
    """
    engine = create_engine(database_url)
    return sessionmaker(engine)


def create_news(Session, records: List[Dict]):
    """

    :param Session:
    :param records:
    :return:
    """
    stmt = insert(news_table).on_conflict_do_nothing('news_un')
    with Session() as session:
        try:
            session.execute(stmt, records)
            session.commit()
        except:
            session.rollback()
            raise


if __name__ == "__main__":
    data = [{
        "news_id": "record.id",
        "url": "record.url",
        "title": "record.title",
        "datetime": "2023-12-16T15:48:00",
        "author": "record.author",
        "news_text": "record.text",
        "provider": "record.provider",
        "source": "record.source",
        "pro_israel_score": 0.3
    }]
    database_url = get_database_url(db_host=os.environ["DB_HOSTNAME"],
                                    db_user=os.environ["DB_USER"],
                                    db_pass=os.environ["DB_USER_PASSWORD"])
    Session = get_session(database_url)

    create_news(Session, data)