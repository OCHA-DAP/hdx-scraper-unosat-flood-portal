## HDX Scraper / Collector Skeleton
This is a skeleton of a Python scraper / collector used by the [Humanitarian Data Exchange](http://data.hdx.rwlabs.org/) project to collect data from the web (i.e. websites or APIs). The scraper is designed to work in a [ScraperWiki](http://scraperwiki.com/) "box", however it can be deployed virtually in any Unix environment.

For detailed documentation about how to create and manage scrapers on ScraperWiki please refer to its official documentation [here](https://scraperwiki.com/help).

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

runsw:
    bash bin/run.sh;
```

The commands are defined as references to shell scripts. Running those commands could be done directly by invoking a call from the terminal: 

```terminal
$ make setup
```

## Setup Structure
The shell script `bin/setup.sh` should contain all the necessary calls for respective setup scripts and also to install the scraper's dependencies. Some scripts may require a database to be setup first, before they are able to run successfully; other require some other special configuration. All of those shoudl be called by the shell script. [`bin/setup.sh`](bin/setup.sh) contains an example:

```shell
#!/bin/bash

#
# Installing dependencies.
#
virtualenv venv
source venv/bin/activate
pip install -r requirements.txt
pip install nose  # for tests

#
# Running collector-specific setup scripts.
#
python tool/scripts/setup/
```

In the example above, the collector-specific scritps will setup the tables of an SQLite database. Click [here](scripts/setup/database.py) to explore that script in more detail.

You can also include crontab configuration in the script above. Here's an example:

```shell
crontab -l | { cat; echo "@daily bash tool/run.sh"; } | crontab -
```
That should configure the collector / scraper to run on a daily schedule.

## Usage Structure
The shell script [`bin/run.sh`](bin/run.sh) contains all the necessary calls to run the script automatically. Here's an example:

```shell
#!/bin/bash

#
# Running the collector / scraper. 
#
source venv/bin/activate
python tool/scripts/example_collect/ > tool/http/log.txt
```

Notice that in the implementation above we are storing the `stdout` on a file called `log.txt`. That file is placed on the folder [`http`](http/) because all the files on that folder are available on the box's API endpoint. It will be available in an URL with the following pattern:

```
> https://ds-ec2.scraperwiki.com/[BOX_ID]/[TOOL_ID]/http/log.txt
```


## Collector / Scraper Structure
The default way to use ScrapeWiki is to store data on a SQLite database. The database has to be named `scraperwiki.sqlite` and it should be placed on the user's root directory. That allows to use a series of features, such as an interactive SQL querier, an html table view with filters, API endpoints for making SQL queries remotedly, etc. There is no configuration necessary for the SQLite database -- it only needs to be placed on the box's root directory: `~/scraperwiki.sqlite`.

Scrapers are generally put inside a directory called `tool/`. The scripts for the scraper should go inside that directory. The `tool/` directory contains five other directories:

```
.
├── config
├── bin
├── data
├── http
├── scripts
└── tests
```

Here is an explanation of each one of these:

* `config` Contains the scraper configuration files. Usually we put a `secrets.json` file that contain HDX API keys together with a `dev.json` and `prod.json` files that contain specific configuration for the scraping task at hand (i.e. API endpoints and table schemas).
* `data` Contains data you may need to use as reference in your scraper. This may be a list of country codes, URLs, etc.
* `http` Generally contains an `index.html` file with the summary of the scraping task and any other files that are intended to be available through an API endpoint, such as a `log.txt` file.
* `scripts` Where the scraper scripts reside.
* `tests` Where the scraper tests reside.

A more detailed folder structure can be found below:

```
.
├── scraperwiki.sqlite
└── tool
    ├── bin
    │   ├── run.sh
    │   ├── runsw.sh
    │   ├── test.sh
    │   ├── setup.sh
    │   └── setupsw.sh
    ├── config
    │   ├── secrets.json
    │   ├── dev.py
    │   └── prod.json
    ├── data
    │   └── country_list.csv
    ├── http
    │   └── index.html
    ├── tests
    │   ├── test_aggregation.py
    │   └── test_database_structure.py
    ├── scripts
    │   ├── example_collect
    │   │   ├── __init__.py
    │   │   ├── __main__.py
    │   │   ├── clean.py
    │   │   ├── collect.py
    │   │   └── patch.py
    │   ├── setup
    │   │   ├── __init__.py
    │   │   ├── __main__.py
    │   │   └── database.py
    │   └── utilities
    │       ├── __init__.py
    │       ├── db.py
    │       └── pretty_print.py
    ├── requirements.txt
    ├── LICENSE.md
    └── README.md
    
```


## Tests Structure
For now, we write our tests using Python's native `unittest`. We use `nose` to run those tests. The shell script `bin/test.sh` should contain all the necessary calls to run the tests you've written:

```shell
#!/bin/bash

#
# Running tests with Nose.
#
source venv/bin/activate
nosetests --with-coverage
```

If time is available, it is *nice* to include tests in your scraper.
