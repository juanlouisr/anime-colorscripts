from bs4 import BeautifulSoup
import re

def main():
    html_document = open("src/html/emojigganime.txt", 'r')

    soup = BeautifulSoup(html_document, 'html.parser')
    
    namelist = []
    count = 0
    for link in soup.find_all('a', 
                            attrs={'href': re.compile("^https://emoji.gg/emoji/")}):
        # skip double/dupe
        count += 1
        if (count % 2 == 0):
            continue    
        scraped_link = str(link.get('href')).strip("https://emoji.gg/emoji/")
        namelist.append(scraped_link)
    
    html_document.close()

    with open("charalist.txt", 'w') as charas:
        for chara in namelist:
            charas.write("%s\n" % chara)


if __name__=='__main__':
    main()