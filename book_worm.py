import requests
import time
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
from bs4 import BeautifulSoup




webdriver_path=r"C:\Users\kesma\Downloads\Compressed\chromedriver.exe"





def crawl(query):

    print("book worm searching: ",query)
    query=query.replace(" ",'+')
    url=r'https://www.mypustak.com/get-books?search='+query
    print("worm geting into web browser")

    driver = webdriver.Chrome(webdriver_path)
    driver.get(url)
    totalcount_div=driver.find_element_by_class_name("total-count")

    totalcount=totalcount_div.text
    totalcount=totalcount.split()
    totalcount=int(totalcount[0])
    if totalcount==0:
        print("sorry no book found of such title")
        driver.close()
    else:
        fetch_count=fetch_enter(totalcount)
        scroll(driver,fetch_count)


def scroll(driver,fetch_count):
    count=int(fetch_count/9)
    while True:
        

        for _ in range(count):
            driver.find_element_by_tag_name("body").send_keys(Keys.PAGE_DOWN)
            time.sleep(5)
        count=1
        text = driver.page_source
        soup = BeautifulSoup(text, "html.parser")
        items = soup.find_all('h3', {'class': 'pro-name'})
        if (len(items) >= fetch_count):
            break
    driver.close()
    print("generating book worm links-price file")
    fetch(items,fetch_count)



def fetch(items,fetch_count):
    x=1
    fw=open("book_worm_generated.html",'w')
    for link in items[:fetch_count]:
        title_string = link.a.string
        title_string = title_string.strip()
        fw.write("<a href='"+link.a['href']+"'>"+str(x) + "." + title_string + "</a><br>\n" )
        print(str(x)+ "."+ title_string)

        price=in_crawl(link.a['href'])
        fw.write("price:"+price+"<br>\n")
        x += 1
    fw.close()


def fetch_enter(totalcount):
    print("total " + str(totalcount) + " books matched to your search how many books details you want to get?")
    fetch_count = 0
    while True:
        try:
            fetch_count = int(input("enter no:"))
            if (fetch_count > totalcount or fetch_count == 0):
                print("please enter a no less than total count")
                continue
            else:
                print("proceeding further")
                break
        except:
            print("enter  a numeric value only")
    return fetch_count


def in_crawl(url):
    source_code = requests.get(url)
    text = source_code.text
    soup = BeautifulSoup(text, "html.parser")
    for link in soup.find_all('span', {'class': 's_cost'}):
        return link.string



crawl(input("which book you want to search for?\n"))

