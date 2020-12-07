import json
import time

from link_finder import geturls
from general import create_project_dir, recipedata, csvjson

def spider(homepage, numofpage, group_name, home_path):
    recipepage = []
    recipepage.append(homepage)

    '''finding urls'''
    for i in range(1, numofpage):
        recipepage.append(homepage + '?page=' + str(i + 1))

    print(recipepage)

    urls = []
    for i in range(len(recipepage)):
        try:
            for m in range(10):
                try:
                    add = geturls(recipepage, i)
                    print('get page ' + str(i) + ' all the recipe urls')
                    time.sleep(0.1)
                    break
                except Exception as e:
                    if m >= 9:
                        print(e)
                    else:
                        time.sleep(0.1)
            urls = urls + add
        except Exception as e:
            break

    '''creating directories'''
    path = home_path +'/' + group_name
    create_project_dir(path)  # '../data/breakfast'
    create_project_dir(path + '/each_' + group_name)  # '../data/breakfast/each_breakfast'
    output = []
    iteration = 0

    '''parsing'''
    while True:
        print('the len of urls is ' + str(len(urls)) + '. the len of output is ' + str(len(output)) + '.')
        if len(output) >= len(urls):
            break
        try:
            print('The input iteration is ' + str(iteration))
            print('The len of urls is ' + str(len(urls)))
            recipedata(iteration, urls, path, group_name)
        except Exception as e:
            print(e)
            print('The current iter is ' + str(iteration) + '. Now input to RecipeJson again.')
            urls.pop(iteration)
            print('The problematic elements in urls has been removed. The len of urls is now ' + str(len(urls)) + '.')

            with open(path + '/' + group_name + '.json', mode='r', encoding='utf-8') as f:
                output = json.load(f)

    '''length check'''
    with open(path + '/' + group_name + '.json', mode='r', encoding='utf-8') as f:
        output = json.load(f)
    print('now the len of output is ' + str(len(output)))
    recipe_name = []
    for i in range(len(output)):
        recipe_name.append(output[i]['recipe_name'])
    setrecipe_name = set(recipe_name)
    print('the number of non-repeatable recipe name is' + str(len(setrecipe_name)))
    if len(setrecipe_name) == len(recipe_name):
        print('no repeatative elements')
    else:
        print('repeatation exists')

    recipe_name = []
    new = []
    for i in range(len(output)):
        if output[i]['recipe_name'] in recipe_name:
            pass
        else:
            recipe_name.append(output[i]['recipe_name'])
            new.append(output[i])
    for i in range(len(new)):
        new[i]['recipe_id'] = i + 1

    with open(path + '/' + group_name + '.json', mode='w', encoding='utf-8') as f:
        json.dump(new, f)

    with open(path + '/' + group_name + '.json', mode='r', encoding='utf-8') as f:
        output = json.load(f)
    print('the len of new output is ' + str(len(output)))

    '''preparation for data processing'''
    output_old = []
    allrecipes_list = [path + '/' + group_name + '.json']  # other json files with same format can be inserted here.
    print(allrecipes_list)
    for i in range(len(allrecipes_list)):
        with open(allrecipes_list[i], mode='r', encoding='utf-8') as f:
            output_old.append(json.load(f))

    '''data processing'''
    csvjson(output_old)
    with open(path + '/' + group_name + '.json', mode='r', encoding='utf-8') as f:
        output = json.load(f)
    print(len(output))
