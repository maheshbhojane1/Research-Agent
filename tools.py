# import os
# import requests
# from langchain.tools import tool
# from bs4 import BeautifulSoup
# from tavily import TavilyClient
# from rich import print
# from dotenv import load_dotenv
# load_dotenv()

# tavily_client = TavilyClient(api_key=os.getenv('TAVILY_API_KEY '))


# @tool

# def web_search(query:str) -> str:
#     """Search the web for recent and relible information on the given topic. Return Titles and URLS"""

#     search_results = tavily_client.search(query = query, max_results=5)

#     out = []

#     for r in search_results['results']:
#         out.append(
#             f'Title: {r['title']}\n'
#             f'URL: {r['url']}\n'
#             f'Snippet: {r['content'][:300]}\n'
#         )

#     return '\n'.join(out)


# # print(web_search.invoke('The trending news in india'))



# @tool
# def scrape(url:str) -> str:
#     """Scrape and return clean content from a given URL from deeper reading"""

#     try:
#         resp = requests.get(url, timeout=8, headers={'User-Agent' : 'Mozilla/5.0'})
#         soup = BeautifulSoup(resp.text, 'html.parser')

#         for tag in  soup(['script', 'style', 'footer', 'nav']):
#             tag.decompose()
        
#         return soup.get_text(separator=' ',strip=True)[:3000]
#     except Exception as e:
#         return f"Error scraping: {str(e)}"

# # print(scrape.invoke('https://www.newindianexpress.com'))

import os
import requests
from langchain.tools import tool
from bs4 import BeautifulSoup
from tavily import TavilyClient
from dotenv import load_dotenv

load_dotenv()

tavily_client = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))


@tool
def web_search(query: str) -> str:
    """Search the web for recent, reliable information on a topic.
    Returns the title, URL and a short snippet for each of the top results.
    Always use this tool to find information; never answer from memory."""
    try:
        results = tavily_client.search(query=query, max_results=5)
    except Exception as e:
        return f"Search failed: {e}"

    out = []
    for r in results["results"]:
        out.append(
            f"Title: {r['title']}\n"
            f"URL: {r['url']}\n"
            f"Snippet: {r['content'][:300]}\n"
        )
    return "\n".join(out)


@tool
def scrape(url: str) -> str:
    """Fetch a web page by URL and return its cleaned text content
    for deeper reading."""
    try:
        resp = requests.get(url, timeout=8, headers={"User-Agent": "Mozilla/5.0"})
        resp.raise_for_status()
        soup = BeautifulSoup(resp.text, "html.parser")
        for tag in soup(["script", "style", "footer", "nav", "header", "aside"]):
            tag.decompose()
        return soup.get_text(separator=" ", strip=True)[:3000]
    except Exception as e:
        return f"Error scraping: {e}"