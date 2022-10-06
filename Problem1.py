
import csv
import urllib
import urllib.request
from bs4 import BeautifulSoup
from selenium import webdriver
opener = urllib.request.build_opener()
opener.addheaders = [('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36'), ('Accept','text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8'), ('Accept-Encoding','gzip, deflate, br'),\
        ('Accept-Language','en-US,en;q=0.5' ), ("Connection", "keep-alive"), ("Upgrade-Insecure-Requests",'1')]
urllib.request.install_opener(opener)  

browser = webdriver.Chrome(r"C:\Users\Dhananjayan\Downloads\chromedriver_win32\chromedriver.exe")
browser.get('https://dermnetnz.org/image-library')

#getting the pagesource and reading the source
pageSource = browser.page_source
soup = BeautifulSoup(pageSource, 'lxml')

# searching for all job containers
location_containers = soup.find_all('a', class_ = 'imageList__group__item')
data=[]
for job in location_containers:
    try:
        temp_dic={}
        temp_dic['URLs associated with diseases'] = job['href']
        disease = job.find(class_="imageList__group__item__copy").text
        disease = disease.replace(" images","").replace("\n","")
        temp_dic['Name of Diseases'] = disease
        src=job.find('img').get('src')
        temp_dic['URLs of Icon images'] = src
        temp_dic['Location of images'] = "Images/{}.png".format(disease.replace(" ","_"))
        urllib.request.urlretrieve(src, "Images/{}.png".format(disease.replace(" ","_")))    
        data.append(temp_dic)
    except:
        pass


info = ['Name of Diseases', 'URLs associated with diseases', 'URLs of Icon images','Location of images']    
with open('Finaldata.csv', 'w+') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames = info)
    writer.writeheader()
    writer.writerows(data)
