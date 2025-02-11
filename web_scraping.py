import json
import bs4
import requests
import pandas as pd
import re
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
import logging
import threading
import time

class jsonInputData:
    title = []
    heading = []
    link = []
    days = []
    date = []
    search_eng = []
    search_string = []

    logging.basicConfig(level=logging.DEBUG, filename='logs.log', format='%(asctime)s %(levelname)s:%(message)s')  # Create log file

    def __init__(self,config_file):
        self.config_file = config_file
        logging.info("Start of program execution") # Logs added to logs.log file
    
    def read_config(self):
        with open(f"{self.config_file}","r") as file:
            jsonData = json.load(file)

        inputList = [[i,j,k] for i in jsonData['input'].get('company') for j in jsonData['input'].get('keywords') for k in range(0, jsonData['input'].get('TotalPages'))]

        # searchEngine = [i for i in jsonData['search_engines']]
        # print(searchEngine)
        # Logs added to logs.log file
        logging.debug("Input list created")

        search_engines = []
        search_engines.append(jsonData['search_engines'].get('google'))
        search_engines.append(jsonData['search_engines'].get('yahoo'))
        search_engines.append(jsonData['search_engines'].get('bing'))


        return inputList, search_engines

    def yahoo(self): 
        inputList, search_engines = self.read_config()

        try:
            for company,keyword,pageno in inputList:
                input_search_string =f'{company} and {keyword}'
                response = requests.get(f"{search_engines[1]}{company}+{keyword}&b={pageno}1&pz=10&xargs=0") # Get information related to the news based on company and keywords
                soup = bs4.BeautifulSoup(response.text, 'lxml')
            
                news = soup.find_all('div',attrs={'class':"dd NewsArticle"})

                for i in news:
                    self.title.append(i.find('h4', attrs={'class':'s-title fz-16 lh-20'}).text) # Title of the article is scraped and stored in title list
                    self.heading.append(i.find('span',attrs={'class':'s-source mr-5 cite-co'}).text) # Publisher of the article is scraped and stored in heading list
                    self.days.append(i.find('span',attrs={'class':'fc-2nd s-time mr-8'}).text) # Date of the article is scraped and stored in days list
                    self.link.append(i.find('h4', class_={'s-title fz-16 lh-20'}).a['href']) # Link of the article is scraped and stored in link list
                    self.search_eng.append('Yahoo') # Search Engine name is stored in search_eng list
                    self.search_string.append(input_search_string) # Input search string is stored in search_string list
                
                logging.debug("Data has been scraped in stored in list") # Logs added to logs.log file
                print("Yahoo")

        except Exception as e:
            #print(e)
            logging.error("Error has occured")

        return self.title, self.heading, self.days, self.link, self.search_eng, self.search_string
        


    def google(self):
        inputList, search_engines = self.read_config()

        try:
            for company,keyword,pageno in inputList:
                input_search_string =f'{company} and {keyword}'
                result = requests.get(f"{search_engines[0]}{company}+{keyword}&tbm=nws&start={pageno}0") # Get information related to the news based on company and keywords
                soup = bs4.BeautifulSoup(result.text,"lxml")

                news_1 = soup.find_all('div', attrs={'class':'Gx5Zad fP1Qef xpd EtOod pkphOe'})
                news_2 = soup.find_all('a', attrs={'class':'tHmfQe'})

                for i in news_1:
                    self.title.append(i.find('h3', attrs={'class':'zBAuLc l97dzf'}).text) # Title of the article is scraped and stored in title list
                    self.heading.append(i.find('div', attrs={'class':'BNeawe UPmit AP7Wnd lRVwie'}).text) # Publisher of the article is scraped and stored in heading list
                    self.days.append(i.find('span', attrs={'class':'r0bn4c rQMQod'}).text) # Date of the article is scraped and stored in days list
                    self.link.append(i.a['href']) # Link of the article is scraped and stored in link list
                    self.search_eng.append('Google') # Search Engine name is stored in search_eng list
                    self.search_string.append(input_search_string) # Input search string is stored in search_string list

                for i in news_2:
                    self.title.append(i.find('h3', attrs={'class':'zBAuLc l97dzf'}).text) # Title of the article is scraped and stored in title list
                    self.heading.append(i.find('span', attrs={'class':'rQMQod aJyiOc'}).text) # Publisher of the article is scraped and stored in heading list
                    self.days.append(i.find('span', attrs={'class':'r0bn4c rQMQod'}).text) # Date of the article is scraped and stored in days list
                    self.link.append(i['href']) # Link of the article is scraped and stored in link list
                    self.search_eng.append('Google') # Search Engine name is stored in search_eng list
                    self.search_string.append(input_search_string) # Input search string is stored in search_string list
                
                logging.debug("Data has been scraped in stored in list") # Logs added to logs.log file   
                print("google")

        except Exception as e:
            #print(e)
            logging.error("Error has occured")
        
        return self.title, self.heading, self.days, self.link, self.search_eng, self.search_string

    def bing(self):
        inputList, search_engines = self.read_config()

        try:
            for company,keyword,pageno in inputList:
                input_search_string =f'{company} and {keyword}'
                 # Get information related to the news based on company and keywords
                response = requests.get(f"{search_engines[2]}{company}+{keyword}urlnews/infinitescrollajax?page={pageno}")
                soup = bs4.BeautifulSoup(response.text, 'lxml')
                        
                news = soup.find_all('div',attrs={'class':"caption"})

                

                for i in news:
                    self.title.append(i.find('a', attrs={'class':'title'}).text) # Title of the article is scraped and stored in title list
                    self.heading.append(i.find('div',attrs={'class':'source set_top'}).text) # Publisher of the article is scraped and stored in heading list
                    self.days.append(i.find('span',attrs={'tabindex':'0'}).text) # Date of the article is scraped and stored in days list
                    self.link.append(i.find('a', class_='title').get('href')) # Link of the article is scraped and stored in link list
                    self.search_eng.append('Bing') # Search Engine name is stored in search_eng list
                    self.search_string.append(input_search_string) # Input search string is stored in search_string list

                logging.debug("Data has been scraped and stored in list") # Logs added to logs.log file
                print("Bing")

        except Exception as e:
            #print(e)
            logging.error("Error has occured")

        return self.title, self.heading, self.days, self.link, self.search_eng, self.search_string

# Convert days list containing information about which hour/day/month/year article was published into datetime
    def convert_to_date(self): 
        day_convert = [i for i in self.days]

        for i in self.days:
            if 'mins' or 'min' or 'm' in i:
                j = int(re.search(r'\d+', i).group())
                self.date.append(str(datetime.now() - timedelta(minutes= j)))
            if 'hours' or 'hour' or 'h' in i:
                j = int(re.search(r'\d+', i).group())
                self.date.append(str(datetime.now() - timedelta(hours= j)))
            if 'days' or 'day' or 'd' in i:
                j = int(re.search(r'\d+', i).group())
                self.date.append(str(datetime.now() - timedelta(days= j)))
            if 'month' or 'months' or 'mon' in i:
                j = int(re.search(r'\d+', i).group())
                self.date.append(str(datetime.now() - relativedelta(months= j)))
            if 'year' or 'years' or 'y' in i:
                j = int(re.search(r'\d+', i).group())
                self.date.append(str(datetime.now() - relativedelta(years= j)))
        # for i in self.date:
        #     print(i)
        logging.debug("Date conversion has been implemented successfully") # Logs added to logs.log file

        return self.date
    
    def dataframe(self): # Create dataframe and export it to csv file
        self.date = self.convert_to_date()

        df = pd.DataFrame(list(zip(self.search_string, self.title, self.heading, self.link, self.date, self.search_eng)), columns=['Search String', 'Title', 'Media', 'Link', 'Date', 'Search Engine']) # Dataframe containing search_string, title, heading, link, date, search_eng is created
        df.to_csv('main.csv') # Convert dataframe to csv file
        print(df.head())

        logging.debug("Dataframe created and exported to csv") # Logs added to logs.log file

        return df


def main(): # Call the methods of class here
    scrapping = jsonInputData("c:\\Users\\yashvardhan_Jadhav\\Desktop\\config.json")

    p1 = threading.Thread(target=scrapping.yahoo)
    p2 = threading.Thread(target=scrapping.google)
    p3 = threading.Thread(target=scrapping.bing)

    p1.start()
    p2.start()
    p3.start()

    p1.join()
    p2.join()
    p3.join()

    # scrapping.yahoo()
    # scrapping.google()
    # scrapping.bing()

    scrapping.dataframe()
    # for i in scrapping.days:
    #     print(i)

if __name__ == "__main__":
    time_start = time.time()
    main()
    time_end = time.time()
    print(f"Time difference: {time_end - time_start}")
