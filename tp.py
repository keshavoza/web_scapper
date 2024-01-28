def bing(self):

    
    inputList = self.read_config()   #Trying too add a comment
    global title
    global heading
    global link
    global days
    
    try:
        for i,j,k in inputList:
            response = requests.get(f"https://www.bing.com/news/search?q={i}+{j}urlnews/infinitescrollajax?page={k}")
            soup = BeautifulSoup(response.text, 'lxml')
                       
            news = soup.find_all('div',attrs={'class':"caption"})

            

            for i in news:
                title.append(i.find('a', attrs={'class':'title'}).text)
                heading.append(i.find('div',attrs={'class':'source set_top'}).text)
                days.append(i.find('span',attrs={'tabindex':'0'}).text)
                link.append(i.find('a', class_='title').get('href'))
                
            ##print("hello")

##            for i in range(len(title)):
##                
##                print(title[i])
##                print(link[i])
##                print(heading[i])
##                print(days[i])

    except :
        logging.error("Error has occured")
