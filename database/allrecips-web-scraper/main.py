import pandas as pd

from spider import spider

model_input = pd.read_excel('model_input.xlsx')

def crawl(homepage, numofpage, group_name, home_path):
    spider(homepage = homepage, numofpage = numofpage,
           group_name = group_name, home_path = home_path)

for i in range(len(model_input)):
    crawl(model_input['homepage'][i], int(model_input['numofpage'][i]),
          model_input['group_name'][i], model_input['home_path'][i])
