# pylint: disable=missing-docstring, line-too-long
import csv
import sys
from os import path
from bs4 import BeautifulSoup
import requests

def parse(html):
    ''' return a list of dict {name, difficulty, prep_time} '''
    soup = BeautifulSoup(html, "html.parser")
    articles = soup.find_all("div", class_="recipe")
    recipes = []
    for article in articles:
        recipes.append(parse_recipe(article))
    return recipes

def parse_recipe(article):
    ''' return a dict {name, difficulty, prep_time} modeling a recipe'''
    recipe_data = article.find("a")
    recipe = {
        "name": recipe_data.get("data-name"),
        "difficulty": recipe_data.find("span", class_="recipe-difficulty").getText(),
        "prep_time": recipe_data.find("span", class_="recipe-cooktime").getText()
    }
    return recipe

def write_csv(ingredient, recipes):
    ''' dump recipes to a CSV file `recipes/INGREDIENT.csv` '''
    with open(f"{ingredient}.csv", "w", encoding="utf-8") as outfile:
        writer = csv.DictWriter(outfile, fieldnames=recipes[0].keys())
        writer.writeheader()
        for recipe in recipes:
            writer.writerow(recipe)

def scrape_from_internet(ingredient):
    ''' Use `requests` to get the HTML page of search results for given ingredients. '''
    all_pages = []
    base_url = "https://recipes.lewagon.com"
    params = {
        "search[query]": {ingredient}
        }
    for i in range(1,4):
        params["page"] = i
        response = requests.get(base_url, params=params)
        if response.status_code > 200:
            print("Something went wrong with the request:", response.url)
        if response.history:
            break
        all_pages.append(response.content)
    return all_pages

def scrape_from_file(ingredient):
    file = f"pages/{ingredient}.html"

    if path.exists(file):
        return open(file, encoding='utf-8')

    print("Please, run the following command first:")
    print(f'curl -g "https://recipes.lewagon.com/?search[query]={ingredient}" > pages/{ingredient}.html')

    sys.exit(1)


def main():
    if len(sys.argv) > 1:
        recipes = []
        ingredient = sys.argv[1]
        all_results = scrape_from_internet(ingredient)
        for result in all_results:
            recipes.extend(parse(result))
        if recipes:
            write_csv(ingredient, recipes)
            print(f"Wrote recipes to recipes/{ingredient}.csv")
        else:
            print("No recipes found.")
    else:
        print('Usage: python recipe.py INGREDIENT')
        sys.exit(0)


if __name__ == '__main__':
    main()
