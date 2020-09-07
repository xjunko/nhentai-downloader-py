import requests, os, subprocess
from bs4 import BeautifulSoup
import re, datetime



class nHentai:
    def __init__(self, id, requests=requests, soup=BeautifulSoup, concurrent_count=20):
        # uncool stuff
        self.id = id
        self.get = requests.get
        self.soup = soup
        self.concurrent_count = 1
        # cool stuff
        self.baseLink = 'https://nhentai.net/g/'
        self.htmlCode = None
        self.scrapeData = None
        self.title = None

        # mp dl
        self.downloaders = None
        self.startTime = datetime.datetime.now()
        self.concurrent_count = concurrent_count # change this if u want to download more at the same time


    def __get_html__(self):
        tempData = self.get(f'{self.baseLink}{self.id}')
        self.htmlCode = tempData.content

    def __scrape_images__(self):
        soup = self.soup(self.htmlCode, features="lxml")
        # get inside the div
        imageDiv = soup.find_all("div", {'id': 'thumbnail-container', 'class':'container'})[0]
        # parse the div
        imageDiv = soup.find_all('div', {"class":'thumb-container'})

        self.scrapeData = [self.convertToHQLink(link.img['data-src']) for link in imageDiv]

        # gets title
        soup = self.soup(self.htmlCode, features="lxml")

        infoDiv = soup.find_all('div', {'id':'info'})[0]
        infoDiv = soup.find_all('h1', {'class':'title'})[0]
        infoDiv = soup.find_all('span', {'class':'pretty'})[0]
        self.title = re.sub('[^\w\-_\. ]', '_', infoDiv.text)
        



    def convertToHQLink(self, url):
        fileformat = url.split('.')[-1]
        fixedID = url.split('.')[-2][:-1].split('/')[-1] # fucked
        removedIDUrl = '/'.join(url.replace('t.', 'i.').split('/')[:-1])
        return f'{removedIDUrl}/{fixedID}.{fileformat}'

    def __save_to_file__(self):
        # crete dir
        if not os.path.exists(f'downloader//[{self.id}]{self.title}'):
            os.makedirs(f'downloader//[{self.id}]{self.title}')

        # save img source to text for wget
        with open(f'downloader//[{self.id}]{self.title}/links.txt', 'w') as file:
            file.write('\n'.join(self.scrapeData))


    def download(self):
        subprocess.call(['aria2c', '-i', f'downloader/[{self.id}]{self.title}/links.txt' , '-d' , f'downloader/[{self.id}]{self.title}/', '-j', f'{self.concurrent_count}'])

    def done(self):
        result = (datetime.datetime.now() - self.startTime).total_seconds()
        print(f'Finished downloading {self.id}, took {result} seconds to download.')





    def run(self):
        self.__get_html__()
        self.__scrape_images__()
        self.__save_to_file__()
        self.download()
        self.done()







