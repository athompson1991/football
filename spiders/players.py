import scrapy
import bs4
from ..items import PassingItem, RushingItem


FOOTBALL_REFERENCE_URL = 'https://www.pro-football-reference.com'

class PassingSpider(scrapy.Spider):

    name = 'passing'
    allowed_domains = ['pro-football-reference.com']

    def __init__(self):
        super().__init__()
        self.years = list(range(1990, 2019))
        self.urls = [FOOTBALL_REFERENCE_URL + "/years/" + str(year) + "/passing.htm" for year in self.years]

    def parse_row(self, row):
        soup = bs4.BeautifulSoup(row.extract())
        tds = soup.find_all('td')
        if(len(tds) > 0):
            link = tds[0].find('a', href=True)['href']
            player_code = link.split('/')[-1]
            player_code = player_code[0:len(player_code) - 4]
            stats = {td["data-stat"]: td.text for td in tds}
            stats['player_code'] = player_code
            stats['player'] = stats['player'].replace('*', '')
            stats['player'] = stats['player'].replace('+', '')
            stats['pos'] = stats['pos'].upper()
            return stats
        else:
            return {}


    def parse(self, response):
        page = response.url
        self.log(page)
        passing = response.css("table#passing")
        passing_rows = passing.css('tr')
        for row in passing_rows[1:]:
            parsed_row = self.parse_row(row)
            if len(parsed_row) != 0:
                parsed_row['season'] = page.split('/')[-2]
                yield PassingItem(parsed_row)

    def start_requests(self):
        for url in self.urls:
            yield scrapy.Request(url=url, callback=self.parse)


class RushingSpider(scrapy.Spider):

    name = 'rushing'
    allowed_domains = ['pro-football-reference.com']

    def __init__(self):
        super().__init__()
        self.years = list(range(1990, 2019))
        self.urls = [FOOTBALL_REFERENCE_URL + "/years/" + str(year) + "/rushing.htm" for year in self.years]

    def parse(self, response):
        page = response.url
        self.log(page)
        rushing = response.css("table#rushing")
        rushing_rows = rushing.css('tr')
        for row in rushing_rows[1:]:
            parsed_row = self.parse_row(row)
            if len(parsed_row) != 0:
                parsed_row['season'] = page.split('/')[-2]
                yield RushingItem(parsed_row)

    def parse_row(self, row):
        soup = bs4.BeautifulSoup(row.extract())
        tds = soup.find_all('td')
        if(len(tds) > 0):
            link = tds[0].find('a', href=True)['href']
            player_code = link.split('/')[-1]
            player_code = player_code[0:len(player_code) - 4]
            stats = {td["data-stat"]: td.text for td in tds}
            stats['player_code'] = player_code
            stats['player'] = stats['player'].replace('*', '')
            stats['player'] = stats['player'].replace('+', '')
            stats['pos'] = stats['pos'].upper()
            return stats
        else:
            return {}

    def start_requests(self):
        for url in self.urls:
            yield scrapy.Request(url=url, callback=self.parse)
