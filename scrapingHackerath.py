from bs4 import BeautifulSoup as soup
from urllib.request import urlopen as uReq
handleString = input()
myUrl='https://www.hackerearth.com/'+handleString
uClient =uReq(myUrl)
page_html=uClient.read()
uClient.close()

f = open("file_hackerearth.txt", "w")

page_soup= soup(page_html,"html.parser")
containerName = page_soup.findAll("span",{"class":"track-following-num"})
#print(len(containerName));
#print(type(containerName))
print("Rating  ",containerName[1].a.text)
f.write(containerName[1].a.text)
#print(soup.prettify(containerName[1]))

f.close()