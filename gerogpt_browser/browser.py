import os
import requests
import requests_cache
import webbrowser
from bs4 import BeautifulSoup
import openai

class GeroGPTBrowser:
    """Simple interface for searching the web and summarizing pages using OpenAI."""

    def __init__(self, openai_api_key=None, *, cache_expire=3600):
        api_key = openai_api_key or os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError(
                "OpenAI API key required. Set OPENAI_API_KEY environment variable or pass via argument."
            )
        # Initialize OpenAI client using the newer library interface
        self.client = openai.OpenAI(api_key=api_key)
        # Cache HTTP requests to speed up repeated searches and summaries
        requests_cache.install_cache("gerogpt_cache", expire_after=cache_expire)

    def search_web(self, query: str, num_results: int = 5):
        """Return a list of search results using DuckDuckGo."""
        url = "https://html.duckduckgo.com/html/"
        headers = {"User-Agent": "Mozilla/5.0"}
        resp = requests.get(url, params={"q": query}, headers=headers)
        soup = BeautifulSoup(resp.text, "html.parser")
        results = []
        for a in soup.select(".result__a")[:num_results]:
            title = a.get_text()
            href = a.get("href")
            results.append({"title": title, "url": href})
        return results

    def summarize_url(
        self,
        url: str,
        *,
        language: str = "English",
        bullets: bool = False,
        sentences: int = 5,
    ):
        """Fetch content from ``url`` and return a short summary."""
        resp = requests.get(url)
        text = resp.text
        prompt_text = text[:4000]  # avoid hitting token limits

        style = " with bullet points" if bullets else ""
        system_prompt = (
            f"Summarize the following text in {language}{style} "
            f"in {sentences} sentences or less."
        )

        completion = self.client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt_text},
            ],
        )

        return completion.choices[0].message.content.strip()

    def open_url(self, url: str):
        """Open a URL in the user's default web browser."""
        webbrowser.open(url)

    def chat(self, prompt: str, language: str = "English"):
        """Send a prompt directly to ChatGPT and respond in the specified language."""
        completion = self.client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are GeroGPT-Browser, a helpful assistant that searches the web and summarizes information."
                    ),
                },
                {"role": "user", "content": f"{prompt}\nRespond in {language}."},
            ],
        )
        return completion.choices[0].message.content.strip()
