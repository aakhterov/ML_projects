import argparse
from bbc_live_news_collector import BBCNewsCollector
from save_to_file import SaveToFile
from classificator import Classificator

if __name__ == "__main__":
    parser = argparse.ArgumentParser("news_collector")
    parser.add_argument("producer", type=str, help="Producer of the news", choices=['bbc'])
    parser.add_argument("path", type=str, help="Path for saving files")
    parser.add_argument("format", type=str, help="Files format", choices=['csv', 'parquet'])
    args = parser.parse_args()

    news = []
    if args.producer == 'bbc':
        bbc_collector = BBCNewsCollector()
        cl = Classificator()

        news = bbc_collector.collect()
        for idx, n in enumerate(news):
            news[idx]["pro_israel_score"] = cl.predict(n["text"])

    saver = SaveToFile()
    path = args.path if args.path[-1] == '/' else args.path + '/'
    if args.format == 'csv':
        saver.save(path, data=news, format='csv')
    else:
        saver.save(path, data=news, format='parquet')
