import scrapy
import bs4
from ..items import PassingItem, RushingItem, ReceivingItem, DefenseItem, KickingItem


FOOTBALL_REFERENCE_URL = 'https://www.pro-football-reference.com'

class PlayerSpider(scrapy.Spider):

    allowed_domains = ['pro-football-reference.com']

    def __init__(self):
        super().__init__()
        self.years = list(range(1990, 2019))

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

    def parse(self, response, target, item_class):
        self.log("parsing row...")
        page = response.url
        table = response.css("table#" + target)
        table_rows = table.css('tr')
        for row in table_rows[1:]:
            parsed_row = self.parse_row(row)
            if len(parsed_row) != 0:
                parsed_row['season'] = page.split('/')[-2]
                yield item_class(parsed_row)

    def start_requests(self):
        for url in self.urls:
            yield scrapy.Request(url=url, callback=self.parse)


class PassingSpider(PlayerSpider):
    name = 'passing'

    def __init__(self):
        super().__init__()
        self.urls = [FOOTBALL_REFERENCE_URL + "/years/" + str(year) + "/passing.htm" for year in self.years]

    def parse(self, response):
        return super().parse(response, target=PassingSpider.name, item_class=PassingItem)

class RushingSpider(PlayerSpider):
    name = 'rushing'

    def __init__(self):
        super().__init__()
        self.urls = [FOOTBALL_REFERENCE_URL + "/years/" + str(year) + "/rushing.htm" for year in self.years]

    def parse(self, response):
        return super().parse(response, target=RushingSpider.name, item_class=RushingItem)

class ReceivingSpider(PlayerSpider):
    name = 'receiving'

    def __init__(self):
        super().__init__()
        self.urls = [FOOTBALL_REFERENCE_URL + "/years/" + str(year) + "/receiving.htm" for year in self.years]

    def parse(self, response):
        return super().parse(response, target=ReceivingSpider.name, item_class=ReceivingItem)

class DefenseSpider(PlayerSpider):
    name = 'defense'

    def __init__(self):
        super().__init__()
        self.urls = [FOOTBALL_REFERENCE_URL + "/years/" + str(year) + "/defense.htm" for year in self.years]

    def parse(self, response):
        return super().parse(response, target=DefenseSpider.name, item_class=DefenseItem)

class KickingSpider(PlayerSpider):
    name = 'kicking'

    def __init__(self):
        super().__init__()
        self.urls = [FOOTBALL_REFERENCE_URL + "/years/" + str(year) + "/kicking.htm" for year in self.years]

    def parse(self, response):
        return super().parse(response, target=KickingSpider.name, item_class=KickingItem)
