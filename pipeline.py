import re
from tools import web_search, scrape
from agent import critic_chain, writer_chain

SEP = "\n" + "== " * 20 + "\n"


def run_research_pipeline(topic: str) -> dict:
    state = {}

    # Step 1 - Search (direct tool call, no agent)
    print(SEP + "Step 1 - Searching ....")
    state["search_result"] = web_search.invoke({"query": topic})
    print("\nsearch result\n", state["search_result"])

    # Step 2 - Read: try the result URLs in order until one scrapes cleanly
    print(SEP + "Step 2 - Reading ....")
    urls = re.findall(r"URL: (\S+)", state["search_result"])
    state["scraped_content"] = ""
    for url in urls:
        text = scrape.invoke({"url": url})
        if not text.startswith("Error scraping") and len(text) > 200:
            state["scraped_content"] = f"Source: {url}\n{text}"
            break
    if not state["scraped_content"]:
        state["scraped_content"] = "No page could be scraped; rely on search snippets."
    print("\nscraped content (preview)\n", state["scraped_content"][:500])

    # Step 3 - Write
    print(SEP + "Step 3 - Writing ....")
    research = (
        f"SEARCH RESULTS:\n{state['search_result'][:2500]}\n\n"
        f"SCRAPED CONTENT:\n{state['scraped_content'][:2500]}"
    )
    state["report"] = writer_chain.invoke({"topic": topic, "research": research})
    print("\nFinal Report\n", state["report"])

    # Step 4 - Critic
    print(SEP + "Step 4 - Critic ....")
    state["feedback"] = critic_chain.invoke({"report": state["report"]})
    print("\ncritic report\n", state["feedback"])

    return state


if __name__ == "__main__":
    topic = input("Enter the topic you want to research: ")
    result = run_research_pipeline(topic)

    print(result)