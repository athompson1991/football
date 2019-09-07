import scrapy
import bs4
from ..items import PassingItem, RushingItem, ReceivingItem, DefenseItem, KickingItem, FantasyItem


FOOTBALL_REFERENCE_URL = 'https://www.pro-football-reference.com'

class PlayerSpider(scrapy.Spider):

    allowed_domains = ['pro-football-reference.com']

    def __init__(self, name):
        super().__init__()
        self.years = list(range(1990, 2019))
        self.urls = [FOOTBALL_REFERENCE_URL + "/years/" + str(year) + "/" + name + ".htm" for year in self.years]

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
            if 'pos' in stats.keys():
                stats['pos'] = stats['pos'].upper()
            if 'catch_pct' in stats.keys():
                stats['catch_pct'] = stats['catch_pct'].replace('%', "")
            if 'fg_perc' in stats.keys():
                stats['fg_perc'] = stats['fg_perc'].replace('%', "")
            if 'fg_perc' in stats.keys():
                stats['xp_perc'] = stats['xp_perc'].replace('%', "")

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
        super().__init__(PassingSpider.name)

    def parse(self, response):
        return super().parse(response, target=PassingSpider.name, item_class=PassingItem)

class RushingSpider(PlayerSpider):
    name = 'rushing'

    def __init__(self):
        super().__init__(RushingSpider.name)

    def parse(self, response):
        return super().parse(response, target=RushingSpider.name, item_class=RushingItem)

class ReceivingSpider(PlayerSpider):
    name = 'receiving'

    def __init__(self):
        super().__init__(ReceivingSpider.name)

    def parse(self, response):
        return super().parse(response, target=ReceivingSpider.name, item_class=ReceivingItem)

class DefenseSpider(PlayerSpider):
    name = 'defense'

    def __init__(self):
        super().__init__(DefenseSpider.name)

    def parse(self, response):
        return super().parse(response, target=DefenseSpider.name, item_class=DefenseItem)

class KickingSpider(PlayerSpider):
    name = 'kicking'

    def __init__(self):
        super().__init__(KickingSpider.name)

    def parse(self, response):
        return super().parse(response, target=KickingSpider.name, item_class=KickingItem)

class FantasySpider(PlayerSpider):
    name = 'fantasy'

    def __init__(self):
        super().__init__(FantasySpider.name)

    def parse(self, response):
        return super().parse(response, target=FantasySpider.name, item_class=FantasyItem)
