# Introduction 
This program is a web scraper that automates the process of gathering information on the outdoor ice-skating rinks from the three largest municipalities of the Waterloo region. 

Please Note: The autoInsert tool will not work in its current form as the database credentials have been removed for security reasons. 

# Getting Started
## Installation process

To enter Python Vitural Environment:

    icy-scraper/.venv/Scripts/Activate.ps1

To install dependencies run command:

    (.venv) $ pip install -r .\requirements.txt

## Software dependencies
icy-scraper is dependent on the following Python libraries:

    * requests
    * BeautifulSoup4
    * pymssql
    * PrettyTable

# Usage
## Scraper

    usage: scraper.py [-h] [-c] [-f] [-s] city
    
    icy-scraper is a web scraper that automates the process of gathering information on the outdoor ice skating rinks from the three largest municipalities of the Waterloo region.
    
    positional arguments:
    city         Name of city to scrape. 'all' for the whole region.
    
    options:
    -h, --help   show this help message and exit
    -c, --count  Will include count in output if flag is present.
    -f, --file   Print JSON scraper results to file.
    -s, --save   Save a local copy of the response(s).

## Auto-Insert

    usage: autoInsert.py [-h] file
    
    This application adds the data collected by icy-scraper to the database.
    
    positional arguments:
    file        Name of the file to load
    
    options:
    -h, --help  show this help message and exit

## Workflow 

The workflow of icy-scraper is as follows:

* Run scraper.py with -f argument so that the scraper can output a JSON file with up-to-date information
    * The files will be saved in scraped_data
* Supply autoInsert.py with that file, and run it.
* Follow the instructions given by autoInsert.py to update the database.

### Note about saving

There are two flags that will allow for the saving of the data that the scraper interacts with.

    -s, --save

-s, will save the HTML from the cities websites 

    -f, --file

-f, will save the resultant JSON to a file in the scraped_data/ directory

## Testing

icy-scraper has automated tests. To run them, just run the script that is native to the operating system that you are using.

    runTests.bat OR runTests.sh
    
# Contributors
[jacnel2](https://github.com/jacnel2)
[SemiDoge](https://github.com/SemiDoge)
