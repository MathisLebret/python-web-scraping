import pandas as pd
import numpy as np
from bs4 import BeautifulSoup
import requests

import re # used to remove footnote indicators
from countryinfo import CountryInfo # used to get countries common names


def clean_text(text):
    '''
    Remove footnote indicators in the text
    '''
    if isinstance(text, str):
        return re.sub(r'\[.*?\]', '', text)
    return text


def common_country_name(country_name):
    '''
    Change official country name to common name
    '''
    country = CountryInfo(country_name)
    return country.name()


def get_infobox(country_name):
    '''
    Get the Wikipedia infobox for a country
    '''
    url = "https://en.wikipedia.org/wiki/" + country_name
    response = requests.get(url)
    html = response.text
    soup = BeautifulSoup(html, 'html.parser')
    infobox = soup.find('table', {'class':'infobox'})
    return infobox


def get_population(infobox):
    variable = None
    for row in infobox.find_all('tr'):
        header = row.find('th')
        if header and 'Population' in header.text:
            # Get the cell of data
            variable_cell = row.find_next_sibling('tr').find('td')
            if variable_cell:
                # Delete footnotes
                variable_text = clean_text(variable_cell.text).strip()
                break
    population = convert_pop(variable_text)
    return population


def convert_pop(population_str):
    population_str = re.sub(r'\s*\(.*\)', '', population_str) # Delete paranthesis including ranks (ex: (20th))
    match = re.search(r'[\d,]+', population_str)
    if match:
        population = match.group(0).replace(',', '')
        return int(population)
    else:
        return np.nan


def get_GDP(infobox):
    variable = None
    for row in infobox.find_all('tr'):
        header = row.find('th')
        if header and 'GDP' in header.text:
            # Get the cell of data
            variable_cell = row.find_next_sibling('tr').find('td')
            if variable_cell:
                # Delete footnotes
                variable_text = clean_text(variable_cell.text).strip()
                break
    gdp_value = convert_gdp(variable_text)
    return gdp_value


def convert_gdp(gdp_str):
    '''
    Used to fix the problem coming from GDP being given in different units on Wikipedia
    '''
    match = re.match(r'[\$\€]?([\d,\.]+)\s*(billion|million|trillion|)\s*.*', gdp_str.strip().lower())
    if not match:
        return np.nan # to notify errors

    # Extract numeric value and unit of measure
    value_str = match.group(1)
    unit = match.group(2)

    # Delete , in numbers
    value = float(value_str.replace(",", ""))

    # Convertion based on unit
    if "billion" in unit:
        return int(value * 1_000_000_000)
    elif "million" in unit:
        return int(value * 1_000_000)
    elif "trillion" in unit:
        return int(value * 1_000_000_000_000)
    else:
        return int(value)


def get_HDI(infobox):
    variable = None
    for row in infobox.find_all('tr'):
        header = row.find('th')
        if header and 'HDI' in header.text:
            # Get the cell of data
            variable_cell = row.find('td')
            if variable_cell:
                # Delete footnotes
                variable_text = clean_text(variable_cell.text).strip()
                break
    HDI = clean_HDI(variable_text)
    return HDI

def clean_HDI(HDI_str):
    match = re.search(r'\d+\.\d+', HDI_str)
    if match:
        return float(match.group(0))
    else:
        return np.nan


def get_currency(infobox):
    variable = None
    for row in infobox.find_all('tr'):
        header = row.find('th')
        if header and 'Currency' in header.text:
            #Get the cell of data
            variable_cell = row.find('td')
            if variable_cell:
                # Delete footnotes
                variable_text = clean_text(variable_cell.text).strip()
                break
    currency = clean_currency(variable_text)
    return currency


def clean_currency(curr_str):
    match = re.search(r'\((\w{3})\)$', curr_str)
    if match:
        return match.group(1)
    else:
        return np.nan


def get_capital(infobox):
    variable = None
    for row in infobox.find_all('tr'):
        header = row.find('th')
        if header and 'Capital' in header.text:
            #Get the cell of data
            variable_cell = row.find('td')
            if variable_cell:
                # Delete footnotes
                variable_text = clean_text(variable_cell.text).strip()
                break
    capital = clean_capital(variable_text)
    return capital


def clean_capital(capital_str):
    match = re.match(r'([a-zA-Z .\'-]+)(?=\s*\d|°|[NSEW]|[0-9])', capital_str)
    if match:
        return match.group(1)
    else:
        return np.nan


def get_language(infobox):
    variable = None
    for row in infobox.find_all('tr'):
        header = row.find('th')
        if header and 'language' in header.text:
            #Get the cell of data
            variable_cell = row.find('td')
            if variable_cell:
                # Delete footnotes
                variable_text = clean_text(variable_cell.text).strip()
                break
    language = clean_language(variable_text)
    return language

def clean_language(language_str):
    language_str = re.sub(r'\s*\(.*\)', '', language_str) #delete None (de jure) or (de facto)
    language_str = re.sub(r'\n', '/', language_str) #replace new lines \n by /
    language_str = re.sub(r'([a-zA-Z]+)([A-Z][a-zA-Z]+)', r'\1/\2', language_str) #joined languages separated by /
    language_str = re.sub(r'^\d+\s*languages:/', '', language_str) #for countries having a list starting from the number of languages
    return language_str
    