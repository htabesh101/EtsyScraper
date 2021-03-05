#### ETSY scraper!
This file will explain the usage of scraper.py

## setup
To run this script please make sure to download the appropriate chrome driver from:
https://chromedriver.chromium.org/downloads

This should match the version of chrome you have installed! Then place this driver in this folder named "chromedriver"!

## Enviroment
I have included a python enviroment with the required python packages!
To enter the enviroment use: 
source py_env/bin/activate

## Running code
To run this code, open the comand line and go to this folder.
Then enter the python enviroment provided with the above command.
Finally run using:
python scraper.py

## inputs
There are 2 types of inputs
    option 1 - a single term
    option 2 - a csv with a column named search_term that contains all search terms

Once the program us ran the terminal will ask for the required information based on option chosen!

# note
Since the script may fail and we dont want to run the search terms we already have, if you enter a output file name that exists, then the script will grab what search terms are in the output file and does not run for those terms!

For example lets say we have the follow list of terms to begin: ["Test1", "Test2", "Test3]

On our first attempt lets say we name the output file name to test.csv. Then if the script fails after finishing "Test2", then on the next run use the same output file name and the script will not retrieve the data for "Test1" and "Test2".

