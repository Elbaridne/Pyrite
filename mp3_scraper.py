from collections import OrderedDict

from bs4 import BeautifulSoup
from selenium import webdriver

#Complete the url
url = "https://URLHERE.xyz/"
attemps = 0


def get_mp3(query):
    '''
    :param query: Artist/Song to search for. It gets transformed in a proper url by the transform_query method Ex. 'Avenged Sevenfold' -> 'https://URLHERE.xyz/Avenged%20Sevenfold
    :return: descargas: dict{'Name of song':'Direct link'} up to a maximum length of 100 results
    :exception TimeOutError: the server might be loading slowly or the webdriver can close prematurely, so it retries up to 3 times
    :exception ValueError: no results for the query

    get_mp3 initializes a selenium webdriver (headless Chrome), and tries to come up with a dictionary of the results yield by the input query
    '''

    # Transform the query in a search result
    url = transform_query(query)

    # Initialize the browser and get the source code
    browser = webdriver.Chrome()
    try:
        browser.get(url)
        html = browser.page_source
        soup = BeautifulSoup(html, 'lxml')

        # Find all the titles and original quality files of the first 100 query results
        titles = [title.text.rstrip('\n\t').lstrip('\n\t') for title in soup.findAll(class_='name')]
        links_originals = list(
            OrderedDict.fromkeys([a['href'] for a in soup.find_all(class_="info-link", href=True) if a.text]))
        if soup.find(class_="list-group-item list-group-item-danger"):
            raise ValueError
        # Prevents the browser from closing before handling the query

        descargas = dict(zip(titles, links_originals))
        if len(descargas) <= 0:
            raise TimeoutError
        else:
            print(descargas)
            return descargas
    except TimeoutError:
        global attemps
        attemps += 1
        print("Retrying... {0} attemp".format(attemps))
        if attemps < 3:
            get_mp3(query)
        else:
            print("TimeOut error, server might be down")

    except ValueError:
        print("No results found!")
    finally:
        browser.close()


def transform_query(query=''):
    if url == "https://URLHERE.xyz/":
        print("You need to complete the url before proceeding!")
    else:
        return url + "?q=" + query.replace(" ", "%20")


if __name__ == '__main__':
    while (True):
        srchqr = input("Artist/Song: ")
        get_mp3(srchqr)
        attemps = 0
