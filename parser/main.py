import time
import requests
from bs4 import BeautifulSoup
from discord import Webhook, RequestsWebhookAdapter, Embed, Colour

def parse():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language':'ru-ru,ru;q=0.8,en-us;q=0.5,en;q=0.3',
        'Accept-Encoding':'gzip, deflate',
        'Connection':'keep-alive',
        'DNT':'1'
    }

    url = 'https://www.avito.ru/sankt-peterburg/avtomobili/renault/logan?f=ASgBAgECAkTgtg2MmSjitg3UqSgBRcaaDBZ7ImZyb20iOjAsInRvIjoxNTAwMDB9&i=1&pmax=150000&pmin=0'
    response = requests.get(url, headers = headers)

    soup = BeautifulSoup(response.content, 'html.parser')
    items = soup.find_all('div', class_ = 'iva-item-root-Nj_hb')
    announcements = []

    for item in items:
        link = item.find('a', class_ = 'link-link-MbQDP')
        if 'sankt-peterburg' in link.get('href'):
            announcements.append({
                'title': link.text,
                'price': item.find('span', class_ = 'price-text-E1Y7h').text,
                'params': item.find('div', class_ = 'iva-item-text-_s_vh').text,
                'geo': item.find('div', class_ = 'geo-georeferences-Yd_m5').text,
                'img': item.find('img', class_ = 'photo-slider-image-_Dc4I'),
                'link': 'https://www.avito.ru/' + link.get('href')
            })

    return announcements

def sendMessage(announcement):
    webhook_url = ''
    webhook = Webhook.from_url(webhook_url, adapter=RequestsWebhookAdapter())
    
    embed = Embed(
                color = Colour.blue(), 
                title = announcement['title']
            )
    embed.set_thumbnail(url = announcement['img']['src'])
    embed.add_field(name = 'Цена', value = announcement['price'])
    embed.add_field(name = 'Параметры', value = announcement['params'])
    embed.add_field(name = 'Местоположение', value = announcement['geo'])
    embed.add_field(name = 'Ссылка', value = announcement['link'])
    
    webhook.send(embed=embed)

def main():
    announcements = parse()

    if announcements:
        print('[INFO]: start')
        for announcement in announcements:
            sendMessage(announcement)
            time.sleep(5)

        print('[INFO]: finished')

if __name__ == '__main__':
    main()