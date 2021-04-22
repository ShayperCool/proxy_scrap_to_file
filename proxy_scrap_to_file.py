from proxyscrape import create_collector
import requests
import threading
import logging

proxies = set()

logpath = "proxies.log"
logger = logging.getLogger('log')
logger.setLevel(logging.INFO)
ch = logging.FileHandler(logpath)
ch.setFormatter(logging.Formatter('%(message)s'))
logger.addHandler(ch)


collector = create_collector('my-collector', 'socks4')

header = {
    'User-Agent': "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36"
    }

def get_proxy():
    proxy_object = collector.get_proxy({'code': 'ru'})
    address = proxy_object.host + ':' + proxy_object.port

    proxy = {
        "http" : "socks4://" + address
    }
    return proxy



def get_working_proxy():
    proxy = get_proxy()
    proxy_finded = False
    while proxy_finded == False:
        try:
            r = requests.get(f"http://example.org", proxies=proxy, headers=header)
            if r.status_code != 200:
                proxy = get_proxy()
            else:
                proxy = proxy["http"][9:]

                if proxies.__contains__(proxy) == False:
                    print(proxy)
                    proxy_finded = True
                    logger.info(proxy)
                    proxies.add(proxy)
                
                proxies.add(proxy)
        except Exception as e:
            proxy = get_proxy()

for i in range(0, 5000):
    x = threading.Thread(target=get_working_proxy)
    x.start()
