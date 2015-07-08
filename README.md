## UNOSAT Flood Portal Scraper
Scraper designed to fetch datasets from [UNOSAT's Flood Portal](http://floods.unosat.org/geoportal/catalog/main/home.page) and create equivalent datasets on HDX.

[![Build Status](https://travis-ci.org/luiscape/hdxscraper-unosat-flood-portal.svg)](https://travis-ci.org/luiscape/hdxscraper-unosat-flood-portal) [![Coverage Status](https://coveralls.io/repos/luiscape/hdxscraper-unosat-flood-portal/badge.svg?branch=master&service=github)](https://coveralls.io/github/luiscape/hdxscraper-unosat-flood-portal?branch=master)

## Resources
* JSON output of the search function: http://floods.unosat.org/geoportal/rest/find/document?rid=local&rids=local&start=1&max=10000&orderBy=relevance&dojo.preventCache=1436368315391&f=json
* Detailed view of datasets: http://floods.unosat.org/geoportal/catalog/search/resource/details.page?uuid=%7B97DFB7B3-BBB8-417A-B97E-91AB213413B4%7D

## Makefile Structure
We are using `Makefiles` to run a series of pre-determined shell scripts. Here is an example of how that `Makefile` should be structured:

```Makefile
test:
    bash bin/test.sh;

setup:
    bash bin/setup.sh;

setupsw:
    bash bin/setup_sw.sh;

run:
    bash bin/run.sh;
```

The commands are defined as references to shell scripts. Running those commands could be done directly by invoking a call from the terminal:

```terminal
$ make setup
```
