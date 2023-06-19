from gevent import monkey
monkey.patch_all()

from crawler.crawl import crawl_and_process

if __name__ == '__main__':
    start_url = input("Enter the page URL to crawl: ")
    max_workers = 5  # Maximum number of gevent workers

    # Crawl the website using the worker
    results = crawl_and_process(start_url,max_workers)

    # Print the results
    for origin, destinations in results.items():
        print(f"URL: {origin}")
        print("Links:")
        for destination in destinations:
            print(destination)
        print()
