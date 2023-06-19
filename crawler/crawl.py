from urllib.parse import urlparse, urljoin
from bs4 import BeautifulSoup
from gevent.pool import Pool
from crawler.utils import WorkerGreenlet


class WorkerPool:
    def __init__(self, max_workers=10):
        self.max_workers = max_workers
        self.pool = Pool(max_workers)
        self.workers = []  # Track acquired workers

    def acquire_worker(self, url):
        # Acquire a worker from the pool
        worker = WorkerGreenlet(url)  # Create a worker greenlet
        self.workers.append(worker)  # Track the acquired worker
        return worker

    def release_worker(self, worker):
        # Release the worker back to the pool
        self.workers.remove(worker)  # Remove the worker from the tracked workers
        worker.kill()  # Terminate the worker greenlet

    def join(self):
        self.pool.join()


def crawl_and_process(start_url, max_worker):
    results = {}

    # Extract the domain from the start URL
    start_domain = get_domain(start_url)

    # Create a set to keep track of visited URLs
    visited_urls = set()

    # Create a worker pool
    worker_pool = WorkerPool(max_worker)

    # Start crawling with the start URL
    crawl_url(start_url, worker_pool, visited_urls, results, start_domain)

    # Wait for all greenlets to complete
    worker_pool.join()

    return results


def crawl_url(url, worker_pool, visited_urls, results, start_domain):
    # Check if the URL has already been visited
    if url in visited_urls:
        return

    # Mark the URL as visited
    visited_urls.add(url)

    # Get the domain of the current URL
    domain = get_domain(url)

    # Check if the URL is within the domain of interest
    if domain != start_domain:
        return

    # Acquire a worker from the worker pool
    worker = worker_pool.acquire_worker(url)

    try:
        # Spawn the worker greenlet to process the URL
        worker.start()

        # Wait for the worker greenlet to complete
        worker.join()

        # Get the response from the worker greenlet
        response = worker.get()

        # Process the response and extract links
        if response and response.text:
            links = extract_links_from_html(response.text, start_domain, url)
            results[url] = links

            # Recursively crawl the extracted links
            for link in links:
                crawl_url(link, worker_pool, visited_urls, results, start_domain)

    finally:
        # Release the worker back to the worker pool
        worker_pool.release_worker(worker)





def get_domain(url):
    parsed_url = urlparse(url)
    return parsed_url.netloc


def extract_links_from_html(html, start_domain, start_url):
    links = []
    soup = BeautifulSoup(html, 'html.parser')
    for anchor in soup.find_all('a'):
        href = anchor.get('href')
        if href:
            # Normalize the URL by joining with the base URL
            absolute_url = urljoin(start_url, href)
            parsed_url = urlparse(absolute_url)
            domain = parsed_url.netloc

            # Check if the URL is within the same domain
            if domain == start_domain:
                links.append(absolute_url)

    return links
