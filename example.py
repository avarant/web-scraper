from scraper import multi_scrape, single_scrape
from bs4 import BeautifulSoup


def main():
    single_scrape("example.html", "https://www.example.com/")


if __name__ == "__main__":
    main()
