from app.fetcher import Fetcher
from app.parser import Parser


def main():
    # Create the fetcher
    fetcher = Fetcher(
        user_agent="KevinKiruiPoliteScraper/1.0",
        contact_url="https://github.com/arapkirui513-hub/polite-scraper",
    )

    # Fetch one page
    response = fetcher.fetch(
        "https://en.wikipedia.org/wiki/Ministry_of_Health_(Kenya)"
    )

    if response is None:
        print("Failed to fetch page.")
        return

    # Parse the HTML
    soup = Parser.parse(response)

    if soup is None:
        print("Failed to parse HTML.")
        return

    # Print the page title
    print("Page title:")
    print(soup.title.text)

    fetcher.close()


if __name__ == "__main__":
    main()