# EPSO

## Intro
The European Personnel Selection Office (EPSO) publishes vacancies in a website, filterable by location, grade, ...
I am not aware of an API, and not aware of a mobile client application to view these vacancies.

As an exercise, I want to create a mobile app showing the same data, in a convenient way.

## Backend
I made an Azure Function that scrapes the website and saves the result in a JSON file.
The function is written in python and uses BeautifulSoup for the scraping.

The Azure Function will run on a schedule in order to periodically update the data (e.g. hourly).
The mobile app will consume the JSON file ( https://jobdata.blob.core.windows.net/jobs/jobs.json )
