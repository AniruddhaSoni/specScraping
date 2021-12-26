import itertools
import requests as req
from bs4 import BeautifulSoup,Tag

extraxt = input("Extract data from?\n1: from mobile name.\n2: from url(only 91mobiles url)\n")

if extraxt == '1':
    mobileName = input("enter Mobile Name: ")
    mobileName=mobileName.replace(" ","-")
    url = f"https://www.91mobiles.com/{mobileName}-price-in-india"
elif extraxt == '2':
    url = input("Enter 91mobiles url\n")

r = req.get(url).text

soup = BeautifulSoup(r, 'lxml')

specsBox = soup.findAll("table", class_="spec_table")[0]

specTitle = specsBox.findAll("td",class_="spec_ttle")
specDes = specsBox.findAll("td",class_="spec_des")

allTitle =[]
allDes = []
i=0
for (title,des) in zip(specTitle,specDes):
    allTitle.append(title.string)
    allDes.append(des.string.replace("  " , '').replace("\n",''))

allIcons=['fa-memory','fa-microchip', 'fa-camera','fa-portrait','fa-battery-full','fa-tv']

f = open("./template.html",'r')
newFile = f.read()

newSoup = BeautifulSoup(newFile ,'lxml')

def template (icon,title,des):
    elements = f"""
        <div class="specs_box processor">
        <i class="fas {icon}"></i>
        <div class="specs_details">
            <h3 class="specs_heading">{title}</h3>
            <span class="key">{des}</span>
        </div>
        </div>
    """
    return elements
specsContainer = newSoup.find("section" , class_="specs_container")

for (icon,title,des) in zip(allIcons,allTitle,allDes):
    element = template(icon,title,des)
    specsContainer.append(element)

newSoup = str(newSoup).replace('&lt;','<').replace('&gt;','>')

f.close()

f = open("./specs.html", 'w')
f.write(newSoup)
f.close()
print("check specs.html in your directory")