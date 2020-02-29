from bs4 import BeautifulSoup as soup
from urllib.request import urlopen as uReq

handleString = input()
myUrl='https://www.hackerrank.com/'+handleString+'?hr_r=1'
uClient =uReq(myUrl)
page_html=uClient.read()
uClient.close()
page_soup= soup(page_html,"html.parser")

f = open("file.txt", "w")

containerName = page_soup.findAll("h1", {"class" : "profile-heading"})

if(len(containerName)!=0):
    print(containerName[0].text)
    f.write(containerName[0].text+"\n")

containerHandle=page_soup.findAll("p", {"profile-username-heading"})
print(containerHandle[0].text)
f.write(containerHandle[0].text+"\n")

containerName2 = page_soup.findAll("p", { "profile-details-value"})

print(containerName2[0].text)
f.write(containerName2[0].text+"\n")
containerBadgeTitle = page_soup.findAll("text", { "badge-title"})

for badges in containerBadgeTitle:
    print(badges.text)
    f.write(badges.text+"\n")
containerBadgeNumber = page_soup.findAll("div", { "hacker-badge"})

print(len(containerBadgeNumber))
for badges in containerBadgeNumber:
    starnumber=badges.findAll("svg",{"badge-star"})
    print(len(starnumber),end=" ")
    i=len(starnumber)
    string=str(i)
    f.write(string+"\n")

f.close()
