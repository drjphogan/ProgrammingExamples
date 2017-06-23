import os
import threading
import requests
from urllib.parse import urlparse, urljoin
from bs4 import BeautifulSoup

from func_tools import singleton as ston


class ImageDownloaderTask:
    """A class for downloading images """
    def run(self, id, proxy):
        print(id, 'starting.')
        download_images(id, proxy)
        # this is total shit
        # this is the second comment

# noinspection PyShadowingNames
def traverse_site(proxy, max_links=20):
    link_parser_singleton = ston.Singleton()

    # While we have pages to parse in queue
    while link_parser_singleton.queue_to_parse:
        # If collected enough links to download images, return
        if len(link_parser_singleton.to_visit) == max_links:
            return

        url = link_parser_singleton.queue_to_parse.pop()

        response = make_http_request(url, proxy)

        # Skip if no usuable response recieved
        if response is None:
            continue

        # Skip if not a web page
        if response.headers['content-type'].find('text/html') < 0:
            continue

        # Add the link to queue for downloading images
        link_parser_singleton.to_visit.add(url)
        print('Added', url, 'to queue')

        bs = BeautifulSoup(response.text, "html.parser")

        for link in BeautifulSoup.findAll(bs, 'a'):
            link_url = link.get('href')

            # <img> tag may not contain href attribute
            if not link_url:
                continue

            parsed = urlparse(link_url)

            # If link follows to external webpage, skip it
            if parsed.netloc and parsed.netloc != parsed_root.netloc:
                continue

            # Construct a full url  from link which can be relative
            link_url = (parsed.scheme or parsed_root.scheme) + '://' + (
                parsed.netloc or parsed_root.netloc) + parsed.path or ''

            # If link was added previously , skip it
            if link_url in link_parser_singleton.to_visit:
                continue

            # Add a link for further parsing
            link_parser_singleton.queue_to_parse = [link_url] + link_parser_singleton.queue_to_parse


# noinspection PyShadowingNames
def make_http_request(url, proxy):

    # get request
    response = requests.get(url, proxies=proxy)
    try:
        response.raise_for_status()
        return response
    except Exception as e:
        print("There was a problem: %s " % str(e))
        return None


def make_valid_file_name(original_name):
    return original_name.replace('%20', '+')


# noinspection PyShadowingNames
def download_images(worker_name, proxy):

    singleton = ston.Singleton()

    # While we have pages where we have not download images
    while singleton.to_visit:

        url = singleton.to_visit.pop()

        print(worker_name, 'Starting downloading images from', url)

        response = make_http_request(url, proxy)

        # Skip if no usuable response recieved
        if response is None:
            continue

        # Skip if not a web page
        if response.headers['content-type'].find('text/html') < 0:
            continue

        bs = BeautifulSoup(response.text, "html.parser")

        # Find all <img> tags
        images = BeautifulSoup.findAll(bs, 'img')

        for image in images:
            # Get image source url which can be absolute or relative
            src = image.get('src')
            # Construct a full url. If the image url is relative
            # it will be prepended with webpage domain
            # If the image url is absolute, it will remain as is
            src = urljoin(url, src)

            # Get a base name, for example 'image.png' to name file locally
            basename = make_valid_file_name(os.path.basename(src))

            if src not in singleton.downloaded:
                singleton.downloaded.add(src)
                print('Downloading', src)
                # Download image to local file system
                download_file(src, proxy, os.path.join('images', basename))

        print(worker_name, 'finished downloading images from', url)


# noinspection PyShadowingNames
def download_file(url, proxy, filename):

    response = make_http_request(url, proxy)
    if response is not None:
        try:
            # open local copy of file in binary mode
            local_file = open(filename, 'wb')
            for chunk in response.iter_content(1000000):
                local_file.write(chunk)

            # close local copy
            local_file.close()
        except FileNotFoundError as e:
            print("There was a problem: %s " % str(e))


if __name__ == "__main__":

    # root = 'http://www.automatetheboringstuff.com'
    # root = 'http://www.python.org'
    root = 'http://www.telegraph.co.uk'
    parsed_root = urlparse(root)

    singleton = ston.Singleton()
    singleton.queue_to_parse = [root]

    # A set of urls to download images from
    singleton.to_visit = set()

    # Downloaded images
    singleton.downloaded = set()

    # For access in the office
    # proxy_details = {"http": "http://127.0.0.1:3128"}
    proxy_details = {}

    traverse_site(proxy_details, 30)

    # Create images directory if not exists
    if not os.path.exists('images'):
        os.makedirs('images')

    # Create new worker classes
    worker1 = ImageDownloaderTask()
    worker2 = ImageDownloaderTask()

    # Create thread for workers to run on
    # thread1 = threading.Thread(target=worker1.run,args=("Thread 1", proxy_details))
    # thread2 = threading.Thread(target=worker2.run,args=("Thread 2", proxy_details))

    thread1 = threading.Thread(target=download_images,args=("Thread 1", proxy_details))
    thread2 = threading.Thread(target=download_images,args=("Thread 2", proxy_details))

    # Start new Threads
    thread1.start()
    thread2.start()
