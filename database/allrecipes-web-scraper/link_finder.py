from urllib.request import urlopen
from bs4 import BeautifulSoup

def geturls(recipepage, page):
    dietpage = urlopen(recipepage[page])
    dietsoup = BeautifulSoup(dietpage,'html.parser')
    urls = []
    recipecard = dietsoup.find_all('div', attrs = {'class':'card__detailsContainer'})
    for i in range(len(recipecard)):
        recipe = recipecard[i]
        recipelink = recipe.find_all('a', attrs = {'class':'card__titleLink manual-link-behavior'})
        for link in recipelink:
            urls.append(link.get('href'))
    return urls
