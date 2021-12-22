## UNOSAT Flood Portal Scraper

ARCHIVED - no longer being run

Scraper designed to fetch datasets from [UNOSAT's Flood Portal](http://floods.unosat.org/geoportal/catalog/main/home.page) and create equivalent datasets on HDX. The resulting datasets, results, and gallery items are created automatically on the [Humanitarian Data Exchange](https://data.hdx.rwlabs.org/organization/un-operational-satellite-appplications-programme-unosat)'s website.

[![Build Status](https://travis-ci.org/OCHA-DAP/hdxscraper-unosat-flood-portal.svg)](https://travis-ci.org/OCHA-DAP/hdxscraper-unosat-flood-portal) [![Coverage Status](https://coveralls.io/repos/OCHA-DAP/hdxscraper-unosat-flood-portal/badge.svg?branch=master&service=github)](https://coveralls.io/github/OCHA-DAP/hdxscraper-unosat-flood-portal?branch=master)

## Setup, Test, and Run
Clone this repository, navigate to the repository's directory, and run:

```shell
$ make setup && make test
$ make run
```

Make sure you edit the config files in the [`config/`](config/) folder if you are interested in having the scripts interact with HDX instances.

## Makefile Structure
This collector makes use of a `Makefile` to run a series of pre-determined shell scripts. The structure of the `Makefile` is presented as follows. Simply run `make` alongside one of the instructions (e.g. `make setup`).

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
