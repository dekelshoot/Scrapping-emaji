from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd
import time
import requests
import sys

def scraping_data(url_page='https://googlefonts.github.io/noto-emoji-animation/',chromedriver='/usr/lib/chromium-browser/chromedriver'):
    print('scraping data...')
    service = webdriver.ChromeService(executable_path = chromedriver)
    driver = webdriver.Chrome(service=service)
    name=[] #List to name of the emoji
    url=[] #List to url of the emoji
    driver.get(url_page)

    # Automatically scroll the page
    scroll_pause_time = 5  # Pause between each scroll
    screen_height = driver.execute_script("return window.screen.height;")  # Browser window height
    i = 1
    while True:
        # Scroll down
        driver.execute_script(f"window.scrollTo(0, {screen_height * i});")
        i += 1
        time.sleep(scroll_pause_time)
    
        # Check if reaching the end of the page
        scroll_height = driver.execute_script("return document.body.scrollHeight;")
        if screen_height * i > scroll_height:
            break

    content = driver.page_source
    soup = BeautifulSoup(content)
    names=[]
    urls=[]
    
    for a in soup.findAll('button',attrs={'class':'is-svg'}): #get all elements with class is-svg
        #get element with class icon-name
        name=a.find('span', attrs={'class':'icon-name'})
        #get get text of this element
        names.append(name.text)
        #get element with class icon-asset
        url = a.find('img', attrs={'class':'icon-asset'})
        #get get url of this element
        urls.append(url.get('src'))

    print('scraping complete!!!')
    return pd.DataFrame({'Name':names,'url svg':urls}) 


def normalize_data(df):
    print('normalizing data ...')
    
    url_gif = []
    url_webp = []
    url_lottie_json = []
    for url in df['url svg']:
        url_gif.append(url.replace('emoji.svg','512.gif'))
        url_webp.append(url.replace('emoji.svg','512.webp'))
        url_lottie_json.append(url.replace('emoji.svg','lottie.json'))
    df['url gif'] = url_gif
    df['url webp'] = url_webp
    df['url littie.json'] = url_lottie_json
    df.to_csv('emoji/emoji.csv', index=False, encoding='utf-8')

    print('normalizing complete!!!')
    return df

def save(df,colonne= 'url gif'):
    print('saving data ...')
    if colonne == "url gif":
        extension = 'gif'
    else:
        if colonne == "url webp":
            extension = 'webp'
        else:
            if colonne == "url svg":
                extension = 'svg'
            else:
                if colonne == "url littie.json":
                    extension = 'json'
    length = df.shape[0]+1
    a = 0
    b = length+1
    percentage = 0
    c = ("\033[93m"+str(percentage)+"% ["+a*"#"+b*"-"+"]"+"\033[0m")
    sys.stdout.write('\r'+c)
    a += 1
    b -= 1
    i = 1
    for index,row in df.iterrows():
        response = requests.get(row[colonne])
        # print(row['url gif'])
        with open('emoji/'+extension+'/'+row['Name']+'.'+extension, 'wb') as f:
            f.write(response.content)
        a += 1
        b -= 1
        percentage = int((i*100)/length)
        c = ("\033[93m"+str(percentage)+"% ["+a*"#"+b*"-"+"]"+"\033[0m")
        sys.stdout.write('\r'+c)
        i += 1
    
    print('data saved!!!')
    