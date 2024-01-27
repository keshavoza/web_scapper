import json
import bs4 
import requests
import pandas as pd
import re
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
import logging

title = []
heading = []
link = []
days = []
date=[]

class jsonInputData:                       
# Configure Logging settings
    logging.basicConfig(level=logging.DEBUG, filename='logs.log', format='%(asctime)s %(levelname)s:%(message)s')

    def __init__(self,config_file):
        #Initializing the class with a config file
        self.config_file = config_file
    
    def read_config(self):
        # Reading the config file
        with open(f"{self.config_file}","r") as file:
            jsonData = json.load(file)
            
            # creating a list of input combinations for formatting the URL
        
        inputList = [[i,j,k] for i in jsonData['input'].get('company') for j in jsonData['input'].get('keywords') for k in range(0,jsonData['input'].get('TotalPages'))]

        # print(inputList)
        return inputList

    def yahoo(self): 
        # title = []
        # heading = []
        # link = []
        # days = []
        search_eng = []
        inputList = self.read_config()  #Retrive input list from configuration file
       
        #Global variables for storing the data
        
        global title
        global heading
        global link
        global days

        try:
            
            # Loop through the input list
            
            for i,j,k in inputList:
                
            # Make request to the Yahoo news search
                
                response = requests.get('https://in.news.search.yahoo.com/search;_ylt=AwrPrHDa8bFlRA4EagfAHAx.;_ylu=Y29sbwNzZzMEcG9zAzEEdnRpZAMEc2VjA3BhZ2luYXRpb24-?q={i}+{j}&b={k}1&pz=10&xargs=0')
                soup = bs4.BeautifulSoup(response.text, 'lxml')
            
                # Find all thenews articles in the response
                
                news = soup.find_all('div',attrs={'class':"dd NewsArticle"})

                for i in news:
                    
                    #Extract title,heading,days,link
                    
                    title.append(i.find('h4', attrs={'class':'s-title fz-16 lh-20'}).text)
                    heading.append(i.find('span',attrs={'class':'s-source mr-5 cite-co'}).text)
                    days.append(i.find('span',attrs={'class':'fc-2nd s-time mr-8'}).text)
                    link.append(i.find('h4', class_={'s-title fz-16 lh-20'}).a['href'])
                print("hello") #Print statement for testing
        

        except:
            # Log an error message if an exception occurs
            logging.error("Error has occured")
        
        return title,heading,days,link

    def google(self):
        #Initialize the list for each search engine data
        search_eng = []
        # Retrieve input list from config file
        inputList = self.read_config()
        
        #Global variables for storing the data
        
        global title
        global heading
        global link
        global days

        try:
            # Loop through the input list
            for i,j,k in inputList:
                # Make a request to Google search 
                result = requests.get(f"https://www.google.com/search?q='{i}'+'{j}'&sca_esv=600979061&rlz=1C1RXQR_enIN1092IN1092&tbm=nws&ei=v6uwZcfjKsOnvr0Pq5So4AQ&start={k}0&sa=N&ved=2ahUKEwiHv7fFsPWDAxXDk68BHSsKCkwQ8tMDegQIBBAE&biw=1318&bih=646&dpr=1")
                soup = bs4.BeautifulSoup(result.text,"lxml")
                
            # Find new articles in the response
                news_1 = soup.find_all('div', attrs={'class':'Gx5Zad fP1Qef xpd EtOod pkphOe'})
                news_2 = soup.find_all('a', attrs={'class':'tHmfQe'})
                
            # Loop through each news article in news_1 
                for i in news_1:
                 #Extract title,heading,days,link
                    
                    title.append(i.find('h3', attrs={'class':'zBAuLc l97dzf'}).text)
                    heading.append(i.find('div', attrs={'class':'BNeawe UPmit AP7Wnd lRVwie'}).text)
                    days.append(i.find('span', attrs={'class':'r0bn4c rQMQod'}).text)
                    link.append(i.a['href'])
            # Loop through each news article in news_2
                for i in news_2:
                    title.append(i.find('h3', attrs={'class':'zBAuLc l97dzf'}).text)
                    heading.append(i.find('span', attrs={'class':'rQMQod aJyiOc'}).text)
                    days.append(i.find('span', attrs={'class':'r0bn4c rQMQod'}).text)
                    link.append(i['href'])

        except:
            # Log an error message if error occurs
            logging.error("Error has occured")
            
            # Return the extracted data
        return title,heading,days,link

    def bing(self):

    # Retrieve the input list from config file
        inputList = self.read_config()

    # Global variables for storing data
        global title
        global heading
        global link
        global days
        
        try:
            #Loop through the input list
            
            for i,j,k in inputList:
                # Make a request to Bing news search
                response = requests.get(f"https://www.bing.com/news/search?q={i}+{j}urlnews/infinitescrollajax?page={k}")
                soup = BeautifulSoup(response.text, 'lxml')
                
                # Find the news articles
                news = soup.find_all('div',attrs={'class':"caption"})

                # Loop through each news article
                 
                for i in news:
                
                    # Extract title,heading,days,link
                    
                    title.append(i.find('a', attrs={'class':'title'}).text)
                    heading.append(i.find('div',attrs={'class':'source set_top'}).text)
                    days.append(i.find('span',attrs={'tabindex':'0'}).text)
                    link.append(i.find('a', class_='title').get('href'))
                    
        except :
            # Log an error message if an exception occurs
            logging.error("Error has occured")

    def convert_to_date(self):
        global days
        global date

        #Loop through each elements in days list
        for i in days:
    
        # Check if 'hours' is present in the days list
            
            if 'hours' in i:
        
        # Extract the number of hours using regex 
                
                j = int(re.search(r'\d+', i).group())
                
        # Append the current date plus the calculated timedelta to 'date' list
                
                date.append(str(datetime.now() - timedelta(hours= j)))
                
        #check if 'days' is present in the current element
            
            elif 'days' in i:
                
        #Extract the number of days using regex
                
                j = int(re.search(r'\d+', i).group())
            
        # Append the current date plus the calculated timedelta to 'date' list 
                
                date.append(str(datetime.now() - timedelta(days= j)))

        # Check if 'month' or 'months' is present in the current element
            
            elif 'month' or 'months' in i:
        
        #Extract the number of months using regex
            
                j = int(re.search(r'\d+', i).group())
                date.append(str(datetime.now() - relativedelta(months= j)))

        #Check if 'Year' or 'Years' is present in the current element
            
            elif 'year' or 'years' in i:
        
        #Extract the number of years using regex
            
                j = int(re.search(r'\d+', i).group())

        # Append the current date plus the calculated relativedelta to 'date' list
                
                date.append(str(datetime.now() - relativedelta(years= j)))

        # return the resulting 'date' list
        return date



def main():
    
# Create an instance of JsonInputData class with the specified configuration file
    
    a = jsonInputData("c:\\Users\\yashvardhan_Jadhav\\Desktop\\config.json")

# Call the yahoo method of the JsonInputData instance

    yahoo=a.yahoo()

#  Call the google method of the JsonInputData instance
    google = a.google()
    print(title)

   
    
if __name__ == "__main__":
    main()




