from scraper import multi_scrape
from bs4 import BeautifulSoup


def parse(html):
    try:
        soup = BeautifulSoup(html, 'html5lib')
        # print(soup.prettify())
        newsContentBlock = soup.find_all(
            "div", {"class": "news-content-block"})
        contentTable = newsContentBlock[0].findAll('p')
        content = []
        for p in contentTable:
            content.append(p.text.strip() + '\n')
        return content
    except:
        # print("PARSE ERROR")
        pass


def main():
    start = 11002
    end = 16002
    base_url = "https://hetq.am/hy/article/"
    prefix = "data/hetqam/"
    filenames = [str(n).zfill(5) for n in range(start, end+1)]
    filepath_url_dict = {prefix + filename +
                         ".txt": base_url + filename for filename in filenames}
    multi_scrape(filepath_url_dict, parse)


if __name__ == "__main__":
    main()
