from bs4 import BeautifulSoup
from lxml import etree
import requests
import re  # instead of wildcards use regular expression to browse days
import json
import datetime as dt


def get_date_from_id(table_id):
    """
    The Studentenwerk-Website (url) generates tables with increasing id's.
    Weekend (Sat/Sun) are ignored in the numeration, so adding just number of
    days to today would fail for next week meals. This function is hackish, but
    works also for meals over 2 or more weeks in the future.
    :param table_id: <id> id-value in "food-plan-{id}"
    :return date: datetime object
    """
    d = dt.timedelta(days=1)
    date = dt.datetime.today()
    for i in range(table_id):
        date += d
        if date.weekday() == 5:  # saturday
            date += 2*d   
    return date


def open_mensa_xml(data_dict):
    """
    converts the data collected in a dictionary to an 
    openmensa feed_v2 compatible xml-string
    """
    xml = etree.Element('openmensa')
    xml.set("version", "2.1")
    xml.set('xmlns', 'http://openmensa.org/open-mensa-v2')
    #xroot.append(etree.Element('innertest'))
    x_ver = etree.SubElement(xml, "version")
    x_ver.text = '5.04-4'
    x_can = etree.SubElement(xml, "canteen")
    for day in data_dict:
        x_day = etree.SubElement(x_can, "day")
        x_day.set("date", day)
        meals = data_dict[day]
        for meal in meals:
            x_cat = etree.SubElement(x_day, "category")
            x_cat.set("name", meal)
            x_mea = etree.SubElement(x_cat, "meal")
            x_name = etree.SubElement(x_mea, "name")
            x_name.text = data_dict[day][meal]["text"] #.replace('&amp;', '&')
            x_pa = etree.SubElement(x_mea, "price")
            x_pa.set('role', 'student')
            x_pa.text = data_dict[day][meal]['A'].replace('€','')
            x_pb = etree.SubElement(x_mea, "price")
            x_pb.set('role', 'employee')
            x_pb.text = data_dict[day][meal]['B'].replace('€','')


            print(meal)
        x_meal = etree.SubElement(x_day, 'meal')
    return etree.tostring(xml, 
        xml_declaration=True, 
        encoding='UTF-8', 
        pretty_print=True
        ).decode('utf-8')


def main(url='https://www.stw-bremen.de/de/essen-trinken/mensa-nw-1', out='xml'):

    # TODO: replace ids with a findall food-plan-* wildcard
    data = {}  # dict to store parsed data
    today = dt.date.today()

    s = requests.session() 
    r = s.get(url)  # get request from stw server
    html = r.content  # the raw html code of the returned page
    soup = BeautifulSoup(html, 'html.parser')  # source code parser

    days = soup.find_all(id=re.compile("^food-plan-"))
    #print(len(days))
    #for id in ids:  # for each day
    for html_day in days:
        date_id = html_day['id']  # food-plan-3
        workday_offset = int(date_id.split('-')[-1])
        #print(workday_offset)
        date = get_date_from_id(workday_offset) 
        date_str = dt.datetime.strftime(date, '%Y-%m-%d')
        data[date_str] = {}  # init dict for each id
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
            data[date_str][category_name] = m
    #print(data)
    j = json.dumps(data, ensure_ascii=False)  # without s saves to file
    #print(j)
    x = open_mensa_xml(data)
    if out == 'xml':
        return x
    elif out == 'json':
        return j

# eventuell musst du dir da noch n .encode('utf8') bzw. zum printen
# .decode('utf8') dranhängen, wenn du utf8 nicht als default encoding hast


if __name__ == '__main__':
    main()
