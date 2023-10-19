import requests
from bs4 import BeautifulSoup
from summarize_t5 import TextSummarization
from urllib.parse import urlparse

def is_url(string):
    try:
        result = urlparse(string)
        return all([result.scheme, result.netloc])
    except ValueError:
        return False
    
def get_wikipedia_text(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
    except requests.exceptions.HTTPError as errh:
        print ("HTTP Error:",errh)
        return None
    except requests.exceptions.ConnectionError as errc:
        print ("Error Connecting:",errc)
        return None
    except requests.exceptions.Timeout as errt:
        print ("Timeout Error:",errt)
        return None
    except requests.exceptions.RequestException as err:
        print ("Something went wrong with the request:",err)
        return None

    soup = BeautifulSoup(response.text, 'html.parser')

    paragraphs = soup.find_all('p')
    text = ' '.join([p.get_text() for p in paragraphs])

    return text

if __name__ == "__main__":
    import argparse

    # Create the parser
    parser = argparse.ArgumentParser(description='Summarize a wikipedia article.')

    # Add the arguments
    parser.add_argument('url', type=str, help='Wikipedia URL to summarize.')
    parser.add_argument('--limit', type=int, default=None, help='Character limit to parse from the article.')

    # Parse the arguments
    args = parser.parse_args()

    # handle arguments
    if not is_url(args.url):
        raise Exception("URL is not valid.")
    
    if args.limit != None and args.limit <= 0:
        raise Exception("Character's limit must be >= 1.")
    
    summarizer = TextSummarization()

    text_wiki = get_wikipedia_text(args.url)

    if args.limit != None:
        text_wiki = text_wiki[:args.limit]

    print(summarizer.summarize_text_t5(text_wiki))