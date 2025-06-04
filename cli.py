import argparse
from gerogpt_browser.browser import GeroGPTBrowser


def main():
    parser = argparse.ArgumentParser(description="GeroGPT-Browser CLI")
    sub = parser.add_subparsers(dest="command", required=True)

    search = sub.add_parser("search", help="Search the web")
    search.add_argument("query", help="Search query")
    search.add_argument("--summarize", action="store_true", help="Summarize the first search result")
    search.add_argument("--open", action="store_true", help="Open the first result in a browser")
    search.add_argument("--num", type=int, default=5, help="Number of results to return")
    search.add_argument("--lang", default="English", help="Language for summaries")
    search.add_argument("--bullets", action="store_true", help="Use bullet points when summarizing")
    search.add_argument("--sentences", type=int, default=5, help="Maximum number of sentences in summaries")

    summ = sub.add_parser("summarize", help="Summarize a web page")
    summ.add_argument("url", help="URL to summarize")
    summ.add_argument("--lang", default="English", help="Language for the summary")
    summ.add_argument("--bullets", action="store_true", help="Use bullet points")
    summ.add_argument("--sentences", type=int, default=5, help="Maximum number of sentences")

    chat = sub.add_parser("chat", help="Send a prompt directly to ChatGPT")
    chat.add_argument("prompt", help="Prompt text")
    chat.add_argument("--lang", default="English", help="Language for the response")

    gui = sub.add_parser("gui", help="Launch the graphical browser")
    gui.add_argument("--incognito", action="store_true", help="Use a private profile")
    gui.add_argument("--dark", action="store_true", help="Enable dark theme")

    args = parser.parse_args()

    browser = GeroGPTBrowser()

    if args.command == "search":
        results = browser.search_web(args.query, num_results=args.num)
        print("Search results:")
        for i, r in enumerate(results, 1):
            print(f"{i}. {r['title']}\n   {r['url']}")
        if args.summarize and results:
            print("\nSummary of first result:")
            summary = browser.summarize_url(
                results[0]["url"],
                language=args.lang,
                bullets=args.bullets,
                sentences=args.sentences,
            )
            print(summary)
        if args.open and results:
            browser.open_url(results[0]["url"])

    elif args.command == "summarize":
        print(
            browser.summarize_url(
                args.url,
                language=args.lang,
                bullets=args.bullets,
                sentences=args.sentences,
            )
        )

    elif args.command == "chat":
        print(browser.chat(args.prompt, language=args.lang))

    elif args.command == "gui":
        from gerogpt_browser.gui import run_gui

        run_gui(incognito=args.incognito, dark=args.dark)


if __name__ == "__main__":
    main()

