import pandas as pd
import numpy as np
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
import random
import psutil
import os

# Reading recipes file. Then select attributes and generate the dataframe for calculation
recipes = pd.read_csv('allrecipes.csv')
recipes = recipes[['recipe_id', 'recipe_name', 'servings',
                      'group_name', 'calories','protein',
                      'carbohydrates', 'fat', 'ingredients', 'recipe_source']]

pattern = re.compile(".+?'(.+?)'")
ingredients = np.zeros(recipes.shape[0])
ingredients = pd.Series(ingredients)
for i in range(recipes.shape[0]):
    temp = pattern.findall(recipes['ingredients'][i])
    temp = '|'.join(temp)
    ingredients[i] = temp
recipes['ingredients'] = ingredients

# Break up the big string into a string array
feature = recipes['group_name'].str.split('|') + recipes['ingredients'].str.split('|')

# Convert to string value
feature = feature.fillna("").astype('str')

# Build a 1-dimensional array with recipe names
recipe_name = recipes['recipe_name']
recipe_source = recipes['recipe_source']
indices = pd.Series(recipes.index, index=recipes['recipe_name'])

# Find similar recipes
def name_recommendations(name, allergy, num_sample, num_recipe):
    # The selected recipe
    idx = indices[name]
    recipe_id = range(len(feature))
    recipe_length = len(feature)
    sample_id = random.sample(recipe_id, num_sample)
    if idx not in sample_id:
        sample_id.append(idx)
        target = sample_id.index(idx)
    else:
        target = sample_id.index(idx)
    sample = feature.iloc[sample_id]
    sample_length = len(sample)
    name_feature = sample
    
    tf = TfidfVectorizer(analyzer='word',ngram_range=(1, 2),min_df=0, stop_words='english')
    tfidf_matrix = tf.fit_transform(name_feature)
    cosine_sim = linear_kernel(tfidf_matrix, tfidf_matrix)
    print(u'Memory usage of current process：%.4f GB' % (psutil.Process(os.getpid()).memory_info().rss / 1024 / 1024 / 1024))

    sim_scores = list(enumerate(cosine_sim[target]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    sim_scores = sim_scores[1:(1+num_recipe)]
    recipe_indices = [name_feature.index[i[0]] for i in sim_scores]
    recipe_indices=list(filter(lambda x:x<=recipe_length, recipe_indices))    
    
    # Remove recieps that the user is allergic to
    user_allergy = allergy.split('|')
    removed_idx = []
    for i in recipe_indices:
        for j in range(len(user_allergy)):
            if user_allergy[j] in recipes['ingredients'][i]:
                print('The user is allergic to this recipe '+ recipe_name.iloc[i])
                removed_idx.append(i)
                break
    for i in range(len(removed_idx)):
        if removed_idx[i] in recipe_indices:
            recipe_indices.remove(removed_idx[i])
    return recipe_indices

def feature_recommendations(like, allergy, num_sample, num_recipe):
    # User's favourite feature
    recipe_id = range(len(feature))
    recipe_length = len(feature)
    sample_id = random.sample(recipe_id, num_sample)
    sample = feature.iloc[sample_id]
    sample_length = len(sample)
    user_like_feature = sample
    temps = like.split('|')

    real_length = len(feature)
    for i in range(len(temps)):
        user_like = pd.Series(str(temps[i].split('&&')))
        user_like_feature[recipe_length + i] = user_like[0]
        real_length = real_length + 1

    # Convert to string value
    user_like_feature_str = user_like_feature.fillna("").astype('str')
    tf = TfidfVectorizer(analyzer='word', ngram_range=(1, 2), min_df=0, stop_words='english')
    user_like_tfidf_matrix = tf.fit_transform(user_like_feature_str)
    print(u'Memory usage of current process：%.4f GB' % (psutil.Process(os.getpid()).memory_info().rss / 1024 / 1024 / 1024))
    user_like_cosine_sim = linear_kernel(user_like_tfidf_matrix, user_like_tfidf_matrix)

    # The index of user_like vector
    union = []
    for i in range(len(temps)):
        idx = len(user_like_feature) - (i + 1)
        sim_scores = list(enumerate(user_like_cosine_sim[idx]))
        sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
        sim_scores = sim_scores[1:(1+num_recipe)]
        recipe_indices = [user_like_feature.index[i[0]] for i in sim_scores]
        recipe_indices=list(filter(lambda x:x<=recipe_length, recipe_indices))

        # Remove recieps that the user is allergic to
        user_allergy = allergy.split('|')
        removed_idx = []
        for i in recipe_indices:
            for j in range(len(user_allergy)):
                if user_allergy[j] in recipes['ingredients'][i]:
                    print('The user is allergic to this recipe ' + recipe_name.iloc[i])
                    removed_idx.append(i)
                    break
        for i in range(len(removed_idx)):
            if removed_idx[i] in recipe_indices:
                recipe_indices.remove(removed_idx[i])
        union.append(recipe_indices)
    return union

if __name__ == "__main__":
    print('Start--------------------')
    user_favorite = 'Chinese Five Spice Spare Ribs'
    user_like = 'ice cream | (salty && Chinese)'
    user_allergy = 'peanut|sesame|lobster'
    num_sample = 5000
    num_recipe = 50
    
    union = feature_recommendations(user_like, user_allergy, num_sample, num_recipe)
    print(union)
    similar_recipes = name_recommendations(user_favorite, user_allergy, num_sample, num_recipe)
    print(similar_recipes)