F = "[main]"


# paso 1
def get_events():
    from crawler import Crawler
    crawler = Crawler()

    print "[main] getting news"
    crawler.get_top_news()

    print "[main] getting festivals"
    crawler.get_festivals()


# paso 2
def get_tweets():
    from dataset_enricher import enrich_festivals, enrich_news, save_tweets, save_pages
    from redis import Redis

    redis = Redis()

    # news tweets
    tweets, pages = enrich_news(redis)

    # festival tweets
    ftweets, fpages = enrich_festivals(redis)

    tweets.extend(ftweets)
    pages.extend(fpages)

    # save tweets
    save_tweets(redis, tweets)

    # save pages
    save_pages(redis, pages)

    # create pages from tweets
    # this downloads and saves pages from tweets text url
    #generate_pages_from(tweets, redis)


# paso 3
def download_pages_from_events():
    from page_downloader import download_pages
    download_pages()


# paso 4
def process_dataset():
    import content_extractor
    from redis import Redis
    redis = Redis()

    content_extractor.process_dataset(redis)


def main():
    print F, "getting news and festivals"
    get_events()

    print F, "getting tweets from news and festivals, and pages from tweets, saving them"
    get_tweets()

    print F, "downloading pages from news"
    download_pages_from_events()

    print F, "extracting content from pages"
    process_dataset()


if __name__ == '__main__':
    main()
