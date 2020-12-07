from urllib.request import urlopen
from bs4 import BeautifulSoup

def geturls(recipepage, page):
    dietpage = urlopen(recipepage[page])
    dietsoup = BeautifulSoup(dietpage,'html.parser')
    urls = []
    recipecard = dietsoup.find_all('div', attrs = {'class':'recipe-card recipeCard'})
    for i in range(len(recipecard)):
        recipe = recipecard[i]
        recipelink = recipe.find_all('a', attrs = {'class':'recipeCard__imageLink'})
        for link in recipelink:
            urls.append(link.get('href'))
    return urls