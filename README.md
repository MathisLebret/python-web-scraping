# Web Scraping of UN Countries Data

## Project Overview

This projects aims at showcasing my skills in **Python** and **web scraping** by collecting country data from infoboxes on Wikipedia.\
The main focus is on demonstrating the technical process of data extraction and preparation, the exact accuracy or utility of the data itself is not critical.

Using **scraping libraries**, this script extracts **public information** that could be used for an econometric study.

The result will be a dataframe where individuals are **UN member countries**, and the variables are:\
    **Qualitative**\
    _ Capital city\
    _ Currency\
    _ Official Language\
    **Quantitative**\
    _ Population\
    _ GDP\
    _ Human Development Index

## Files included

1. A **Jupyter notebook** called 'WebScraping.ipynb' with the whole process.
2. A **Python module** named 'CountryScraping.py' containing the long and repetitive functions.
3. A **CSV file** with the collected data, ready for analysis.

## What I learned through this project

Basics of web scraping with **BeautifulSoup**.\
Working with **raw,unstructured web data**.\
**Cleaning data** and especially character chains.\
**Project management** and **presenting results**.

## Known Issues

_For some countries, the infobox could not be scraped. Only 6.2% of countries are concerned.\
_Currency resulted in NaN for some countries.\
_Another problem was encountered for some countries because list of languages are very different from one Wikipedia page to another.\
I plan to fix those problems later.

## Author

**Mathis Lebret** - *Student in the first year of a Master in Econometrics and Statistics at ISFA Lyon.*\
Link to my **[LinkedIn Profile](www.linkedin.com/in/mathis-lebret-566952190)**.