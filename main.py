from requests import session
from bs4 import BeautifulSoup
from json import load
from os import environ

with open('config.json', 'r') as f: DATA = load(f)
def getenv(var): return environ.get(var) or DATA.get(var, None)


UPTOBOX_TOKEN = getenv("UPTOBOX_TOKEN")
ndus = getenv("TERA_COOKIE")
if ndus is None: TERA_COOKIE = None
else: TERA_COOKIE = {"ndus": ndus}

def terabox(url) -> str:
    sess = session()

    # Example URL provided as an argument
    # url = 'https://www.example.com'

    while True:
        try: 
            res = sess.get(url)
            print("connected")
            break
        except: 
            print("retrying")
    
    key = res.url.split('?surl=')[-1]
    url = f'http://www.terabox.com/wap/share/filelist?surl={key}'
    sess.cookies.update(TERA_COOKIE)

    while True:
        try: 
            res = sess.get(url)
            print("connected")
            break
        except Exception as e: 
            print("retrying")

    key = res.url.split('?surl=')[-1]
    soup = BeautifulSoup(res.content, 'lxml')
    jsToken = None

    for fs in soup.find_all('script'):
        fstring = fs.string
        if fstring and fstring.startswith('try {eval(decodeURIComponent'):
            jsToken = fstring.split('%22')[1]

    while True:
        try:
            res = sess.get(f'https://www.terabox.com/share/list?app_id=250528&jsToken={jsToken}&shorturl={key}&root=1')
            print("connected")
            break
        except: 
            print("retrying")
    
    result = res.json()

    if result['errno'] != 0: 
        return f"ERROR: '{result['errmsg']}' Check cookies"

    result = result['list']
    if len(result) > 1: 
        return "ERROR: Can't download multiple files"

    result = result[0]
    if result['isdir'] != '0':
        return "ERROR: Can't download folder"

    return result.get('dlink', "Error")

# Usage: Call the function with the desired URL
# Example usage:
# download_link = terabox('https://www.example.com')
