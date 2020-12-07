from urllib.request import urlopen
from bs4 import BeautifulSoup
import re
import time

class recipeinfo:
    def __init__(self, url):
        for i in range(10):
            try:
                self.recipepage = urlopen(url)
                time.sleep(0.1)
                break
            except Exception as e:
                if i >= 9:
                    print(e)
                else:
                    time.sleep(0.1)
        self.recipesoup = BeautifulSoup(self.recipepage, 'html.parser')

    def getname(self):
        self.name = self.recipesoup.find(attrs={'class': 'headline heading-content'})
        try:
            self.name = self.name.string
        except AttributeError:
            self.name = 'unknown'
        self.name = self.name.replace('/', ' or ')
        self.name = self.name.replace('"', '')
        return self.name

    def getsummary(self):
        try:
            self.summary = self.recipesoup.find(attrs={'class': 'recipe-summary margin-8-bottom'})
        except Exception as e:
            print(e)
            self.summary = 'not known'
        try:
            self.paragraph = self.summary.find(attrs={'class': 'margin-0-auto'})
            self.paragraph = self.paragraph.string
        except Exception as e:
            print(e)
            self.paragraph = 'not known'
        return self.paragraph

    '''Yes'''

    def getauthor(self):
        self.author = self.recipesoup.find(attrs={'class': 'author-name link'})
        try:
            self.author = self.author.string
        except AttributeError:
            self.author = 'unknown'
        try:
            self.authorlink = self.author.get('href')
        except AttributeError:
            self.authorlink = 'unknown'
        return self.author
        return self.authorlink

    def getrecipeinfo(self):
        try:
            self.recipeinfo = self.recipesoup.find_all(attrs={'class': 'recipe-meta-item-body'})
            self.infolist = []
            for info in self.recipeinfo:
                info = info.string
                info = info.replace('\n', '')
                info = re.sub(' +', ' ', info)
                info = info.strip()
                self.infolist.append(info)
            self.infolist[-2] = int(self.infolist[-2])
        except Exception as e:
            print(e)
            self.infolist = [1, 'none']
        return self.infolist

    def getingredients(self):
        try:
            self.ingredients = self.recipesoup.find_all(attrs={'class': 'ingredients-item-name'})
            self.ingredientslist = []
            for ingredient in self.ingredients:
                self.ingredientslist.append(ingredient.string)

            for i in range(len(self.ingredientslist)):
                self.ingredientslist[i] = self.ingredientslist[i].replace('\n', '')
                self.ingredientslist[i] = re.sub(' +', ' ', self.ingredientslist[i])
                self.ingredientslist[i] = self.ingredientslist[i].strip()
        except Exception as e:
            print(e)
            self.ingredientslist = ['not known']
        return self.ingredientslist

    def getdirections(self):
        try:
            self.directions = self.recipesoup.find_all(attrs={'class': 'subcontainer instructions-section-item'})
            self.directionslist = []
            for direction in self.directions:
                direction = direction.find('div')
                direction = direction.find('p')
                direction = direction.string
                self.directionslist.append(direction)
        except Exception as e:
            print(e)
            self.directionslist = ['not known']
        return self.directionslist

    def getnutrition(self):
        try:
            self.nutrition = self.recipesoup.find(attrs={'class': 'partial recipe-nutrition-section'})
            self.nutrition = self.nutrition.find(attrs={'class': 'section-body'})
            self.nutrition = self.nutrition.text
            self.nutrition = self.nutrition.replace('Full Nutrition\n', '')
            self.nutrition = re.sub(' +', ' ', self.nutrition)
            self.nutrition = self.nutrition.strip()
            self.nutritionlist = self.nutrition.split(';')
        except Exception as e:
            print(e)
            self.nutritionlist = [0, 0, 0, 0, 0, 0]
        self.nutritionfact = []
        for i in range(len(self.nutritionlist)):
            if i == 0:
                self.nutritionlist[i] = self.nutritionlist[i].replace(' calories', '')
                try:
                    self.nutritionlist[i] = float(self.nutritionlist[i])
                except Exception:
                    self.nutritionlist[i] = 0
                self.nutritionfact.append(self.nutritionlist[i])
            if i == 1:
                self.nutritionlist[i] = self.nutritionlist[i].replace(' protein ', '')
                self.nutritionlist[i] = self.nutritionlist[i].replace(' DV', '')
                temp = self.nutritionlist[i].split('g')
                try:
                    temp[1] = temp[1].strip()
                    temp[0] = float(temp[0])
                except Exception:
                    temp[0] = 0
                self.nutritionfact.append(temp[0])
            if i == 2:
                self.nutritionlist[i] = self.nutritionlist[i].replace(' carbohydrates ', '')
                self.nutritionlist[i] = self.nutritionlist[i].replace(' DV', '')
                temp = self.nutritionlist[i].split('g')
                try:
                    temp[1] = temp[1].strip()
                    temp[0] = float(temp[0])
                except Exception:
                    temp[0] = 0
                self.nutritionfact.append(temp[0])
            if i == 3:
                self.nutritionlist[i] = self.nutritionlist[i].replace(' fat ', '')
                self.nutritionlist[i] = self.nutritionlist[i].replace(' DV', '')
                temp = self.nutritionlist[i].split('g')
                try:
                    temp[1] = temp[1].strip()
                    temp[0] = float(temp[0])
                except Exception:
                    temp[0] = 0
                self.nutritionfact.append(temp[0])
            if i == 4:
                self.nutritionlist[i] = self.nutritionlist[i].replace(' cholesterol ', '')
                self.nutritionlist[i] = self.nutritionlist[i].replace(' DV', '')
                temp = self.nutritionlist[i].split('mg')
                try:
                    temp[1] = temp[1].strip()
                    temp[0] = float(temp[0])
                except Exception:
                    temp[0] = 0
                self.nutritionfact.append(temp[0])
            if i == 5:
                self.nutritionlist[i] = self.nutritionlist[i].replace(' sodium ', '')
                self.nutritionlist[i] = self.nutritionlist[i].replace(' DV', '')
                temp = self.nutritionlist[i].split('mg')
                try:
                    temp[1] = temp[1].strip()
                    temp[0] = float(temp[0])
                except Exception:
                    temp[0] = 0
                self.nutritionfact.append(temp[0])
        return self.nutritionfact

