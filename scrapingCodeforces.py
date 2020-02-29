from bs4 import BeautifulSoup as soup
from urllib.request import urlopen as uReq
handleString = input()
myUrl='http://codeforces.com/profile/'+handleString
uClient =uReq(myUrl)
page_html=uClient.read()
uClient.close()

f = open("file_codeforces.txt", "w")

page_soup= soup(page_html,"html.parser")
containerName = page_soup.findAll("div", {"user-rank"})
#print(soup.prettify(containerName[0]))
#print(len(containerName[]))
print(containerName[0].span.text,"1")
f.write(containerName[0].span.text+"\n")
UserBox = page_soup.findAll("div", {"userbox"})
#print(soup.prettify(UserBox[0]))
lists = UserBox[0].findAll("li")

#print(len(lists)) 
maxPupil = lists[0].findAll("span")
for span in maxPupil:
    print(span.text)
    f.write(span.text+"\n") 

print("contribution=",lists[1].span.text)
f.write("contribution="+lists[1].span.text)

f.close()