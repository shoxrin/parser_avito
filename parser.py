import requests
from bs4 import BeautifulSoup


class Parser:
    def __init__(self):
        self.headers = {
            'Referer': 'https://www.google.com/',
            'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.71 Safari/537.36',
            'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language':'ru,en-US;q=0.5',
            'Accept-Encoding':'gzip, deflate, br',
            'DNT':'1',
            'Connection':'keep-alive',
            'Upgrade-Insecure-Requests':'1',
            'Pragma':'no-cache',
            'Cache-Control':'no-cache'
        }
        self.session = requests.Session()

    def getHTML(self, url):
        response = self.session.get(url=url, headers=self.headers)
        soup = BeautifulSoup(response.content, 'html.parser')
        items = soup.find_all('div', class_ = 'iva-item-root-Nj_hb')
        print('[STATUS_CODE]:', response.status_code)

        return items

    def getAnnouncements(self, url):
        items = self.getHTML(url)
        announcements = []
        tmp = ''
        for item in items:
            link = item.find('a', class_ = 'link-link-MbQDP')
            date = item.find('div', class_ = 'date-text-VwmJG').text
            if ('Несколько секунд назад' == date) and link.get('href') != tmp:
                tmp = link.get('href')
                announcements.append({
                    'title': link.text,
                    'price': item.find('span', class_ = 'price-text-E1Y7h').text,
                    'params': item.find('div', class_ = 'iva-item-text-_s_vh').text,
                    'geo': item.find('div', class_ = 'geo-georeferences-Yd_m5').text,
                    'img': item.find('img', class_ = 'photo-slider-image-_Dc4I'),
                    'link': 'https://www.avito.ru' + link.get('href')
                })
            else:
                break

        return announcements