# Website Crawler

The Website Crawler is a Python application that crawls a website starting from a given URL and extracts all the internal links within the same domain. It utilizes the Gevent library for concurrent and asynchronous crawling.

## Features

- Concurrent and asynchronous crawling using Gevent.
- Extracts internal links within the same domain.
- Handles relative and absolute URLs.
- Prevents duplicate crawling of URLs.
- User-defined maximum number of concurrent workers.

## Prerequisites

- Python 3.9
- Gevent library


## Usage

1. Run the `main.py` script:

```shell
python main.py
```

2. Enter the starting URL when prompted.

3. The crawler will start crawling the website and extract the internal links.

4. The results will be displayed in the console, showing the origin URL and the extracted links.

## Configuration

You can configure the maximum number of concurrent workers by modifying the `max_workers` variable in the `main.py` script. The default value is 5.

## Structure

The project structure is organized as follows:

- `main.py`: Entry point of the application. It prompts for the starting URL and initiates the crawling process.
- `crawler/crawl.py`: Contains the main crawling logic, including acquiring and releasing workers, crawling URLs, and extracting links from HTML.
- `crawler/utils.py`: Defines the `WorkerGreenlet` class, which extends the `gevent.Greenlet` class and performs the HTTP requests.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

