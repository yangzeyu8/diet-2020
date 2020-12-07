import os
import pandas as pd
import json

from parser import recipeinfo

# Each website is a separate project (folder)
def create_project_dir(directory):
    if not os.path.exists(directory):
        print('Creating directory ' + directory)
        os.makedirs(directory)

def recipedata(start, urls, path, group_name):
    '''########################## Make changes ############################'''
    global iteration
    global output
    table = pd.DataFrame(columns=[
        'model', 'recipe_id', 'recipe_name', 'servings', 'group_name', 'calories',
        'protein', 'carbohydrates', 'fat', 'ingredients', 'recipe_source'
    ])

    each = pd.DataFrame(columns=[
        'model', 'recipe_id', 'recipe_name', 'servings', 'group_name', 'calories',
        'protein', 'carbohydrates', 'fat', 'ingredients', 'recipe_source'
    ])

    for recipeid in range(start, len(urls)):
        iteration = recipeid
        print('Scraping the ' + str(recipeid) + 'th' + ' recipe')

        information = recipeinfo(urls[recipeid])
        information.getname()
        information.getsummary()
        information.getauthor()
        information.getrecipeinfo()
        information.getingredients()
        information.getdirections()
        information.getnutrition()

        data = {'model': 'recipes.recipe',
                'recipe_id': recipeid + 1,
                'recipe_name': information.name,
                'servings': information.infolist[-2],
                'group_name': group_name,
                'calories': information.nutritionfact[0],
                'protein': information.nutritionfact[1],
                'carbohydrates': information.nutritionfact[2],
                'fat': information.nutritionfact[3],
                'ingredients': information.ingredientslist,
                'recipe_source': urls[recipeid]
                }
        output.append(data)
        print('the len of urls is ' + str(len(urls)) + '. the len of output is ' + str(len(output)) + '.')

        print('Save the accumulated recipes until the ' + str(recipeid) + 'th' + ' recipe to JSON format')
        with open(path + '/' + group_name + '.json', mode='w', encoding='utf-8') as f:
            json.dump(output, f)

        print('Save the ' + str(recipeid) + 'th' + ' recipe to CSV format')

        each = each.append(
            [{'recipe': group_name + '-' + str(recipeid + 1), 'model': 'recipes.recipe', 'recipe_id': recipeid + 1,
              'recipe_name': information.name, 'servings': information.infolist[-2],
              'group_name': group_name,
              'calories': information.nutritionfact[0],
              'protein': information.nutritionfact[1],
              'carbohydrates': information.nutritionfact[2],
              'fat': information.nutritionfact[3],
              'ingredients': information.ingredientslist,
              'recipe_source': urls[recipeid]}], ignore_index=True)

        each.to_csv(path + '/each_' + group_name + '/' + information.name + '.csv')
        each = pd.DataFrame(columns=[
            'model', 'recipe_id', 'recipe_name', 'servings', 'group_name', 'calories',
            'protein', 'carbohydrates', 'fat', 'ingredients', 'recipe_source'
        ])
        print('Save the accumulated recipes until the ' + str(recipeid) + 'th' + ' recipe to CSV format')
        table = table.append(
            [{'recipe': group_name + '-' + str(recipeid + 1), 'model': 'recipes.recipe', 'recipe_id': recipeid + 1,
              'recipe_name': information.name, 'servings': information.infolist[-2],
              'group_name': group_name,
              'calories': information.nutritionfact[0],
              'protein': information.nutritionfact[1],
              'carbohydrates': information.nutritionfact[2],
              'fat': information.nutritionfact[3],
              'ingredients': information.ingredientslist,
              'recipe_source': urls[recipeid]}], ignore_index=True)
        table.to_csv(path + '/' + group_name + '.csv')
        if len(output) >= len(urls):
            break

    print('Save all recipes as JSON file')
    with open(path + '/' + group_name + '.json', mode='w', encoding='utf-8') as f:
        json.dump(output, f)
        # 将字典列表存入json文件中


'''this function is to merge separate json files into one json file and another csv file'''


def csvjson(allrecipes, path, group_name):
    output = []
    table = pd.DataFrame(index=[
        'model', 'recipe_id', 'recipe_name', 'servings', 'group_name', 'calories',
        'protein', 'carbohydrates', 'fat', 'ingredients', 'recipe_source'
    ])

    '''for allrecipes.com'''
    for i in range(len(allrecipes)):
        for recipeid in range(len(allrecipes[i])):
            data = {'model': 'recipes.recipe',
                    'recipe_id': recipeid + 1,
                    'recipe_name': allrecipes[i][recipeid]['recipe_name'],
                    'servings': int(allrecipes[i][recipeid]['servings']),
                    'group_name': allrecipes[i][recipeid]['group_name'],
                    'calories': float(allrecipes[i][recipeid]['calories']),
                    'protein': float(allrecipes[i][recipeid]['protein']),
                    'carbohydrates': float(allrecipes[i][recipeid]['carbohydrates']),
                    'fat': float(allrecipes[i][recipeid]['fat']),
                    'ingredients': allrecipes[i][recipeid]['ingredients'],
                    'recipe_source': allrecipes[i][recipeid]['recipe_source'],
                    }
            output.append(data)

            table[allrecipes[i][recipeid]['group_name'] + '-id' + str(recipeid + 1)] = [
                'recipes.recipe', recipeid + 1, allrecipes[i][recipeid]['recipe_name'],
                int(allrecipes[i][recipeid]['servings']),
                allrecipes[i][recipeid]['group_name'],
                float(allrecipes[i][recipeid]['calories']),
                float(allrecipes[i][recipeid]['protein']),
                float(allrecipes[i][recipeid]['carbohydrates']),
                float(allrecipes[i][recipeid]['fat']), allrecipes[i][recipeid]['ingredients'],
                allrecipes[i][recipeid]['recipe_source']
            ]

    table = table.stack()
    table = table.unstack(0)
    table.to_csv(path + '/' + group_name + '.csv')

    print('Save as JSON file')
    with open(path + '/' + group_name + '.json', mode='w', encoding='utf-8') as f:
        json.dump(output, f)