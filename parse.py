from bs4 import BeautifulSoup
import requests
import re  # instead of wildcards use regular expression to browse days
import json


url = 'https://www.stw-bremen.de/de/essen-trinken/mensa-nw-1'
# TODO: replace ids with a findall food-plan-* wildcard
data = {}  # dict to store parsed data

s = requests.session() 
r = s.get(url)  # get request from stw server
html = r.content  # the raw html code of the returned page
soup = BeautifulSoup(html, 'html.parser')  # source code parser

days = soup.find_all(id=re.compile("^food-plan-"))
#print(len(days))
#for id in ids:  # for each day
for day in days:
    # TODO: parse date from table string or recalc from id?
    # TODO: rename id to date or day or whatever?
    id = day['id']
    data[id] = {}  # init dict for each id
    html_day = soup.find_all(id=id)  # array with code snippets for each day
    if len(html_day) > 1: 
        print('WARNING: more than one tags with id ' + id + 'found')
    elif len(html_day) <1:
        print('ERROR: no tags with id ' + id + 'found')
    html_day = html_day[0]
    # The information for each meal is stored in a seperate table with class
    # food-category, to get all categories (not hardcoded loop them)
    html_meals = html_day.find_all("table", "food-category")
    for meal in html_meals:
        # meal is still a html code string
        category_name = meal.find('th', 'category-name').string
        meal_text = ''
        # since there are added line breaks and <sup> tags, I use the strings
        # generator instead of the get_text() or .text methods
        meal_parts = meal.find('td', 'field-name-field-description').strings
        for m in meal_parts:  # m is an iteratable part of the html contents
            if not m.parent.name == 'sup':
                meal_text += str(m)
        #meal_text = meal_text.rstrip()  # remove win/unix linebreaks
        meal_text = meal_text.replace('\r', '')
        meal_text = meal_text.replace('\n', ' ')
        meal_text = meal_text.replace('* * *', '; ')
        meal_price_a = meal.find('td', 'field-name-field-price-students').text
        meal_price_b = meal.find('td', 'field-name-field-price-employees').text
        
        m = {}
        m['text'] = meal_text
        m['A'] = meal_price_a
        m['B'] = meal_price_b
        data[id][category_name] = m
print(data)
j = json.dumps(data, ensure_ascii=False)  # without s saves to file
print(j)

# eventuell musst du dir da noch n .encode('utf8') bzw. zum printen
# .decode('utf8') dranhängen, wenn du utf8 nicht als default encoding hast
