from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import WebDriverException
import time 
import pandas as pd
import os

class etsy():
    base_url = "https://www.etsy.com/ca/"
    chrome_driver_loc = "chromedriver"

    def __init__(self):
        self.options = webdriver.ChromeOptions()
        self.options.add_argument('--headless')
        self.options.add_argument('--no-sandbox')
        self.options.add_argument('window-size=1920x1080')
        self.driver = webdriver.Chrome(self.chrome_driver_loc, options=self.options)
        
    def get_combinations(self, listA, listB):
        output = []
        for i in listA:
            for j in listB:
                output.append(i + " " + j)
        return output

    def get_listing_info(self, search_term, url, df, df_i):
        try:
            self.driver.get(url)
        except WebDriverException:
            self.driver = webdriver.Chrome(self.chrome_driver_loc, options=self.options)
            self.driver.get(url)

        print("url = " + url)
        time.sleep(2)

        # lets check if the item is still available
        try:
            not_found = self.driver.find_element_by_xpath('//*[@id="content"]/div/div[1]/div/div/div/p')
            return False
        except:
            pass
        
        # Lets see if the item is on break!
        try:
            on_break = self.driver.find_element_by_xpath('//*[@id="content"]/div/div[1]/div/div/div[2]/div[2]/div[1]/div/div/p').text
            return False
        except:
            pass
        
        try:
            div_i = 0 
            title = self.driver.find_element_by_xpath('//*[@id="listing-page-cart"]/div/div['+str(2+div_i)+']/div/h1')
            listing_id = title.get_attribute('data-listing-id')
            title = title.text         
            # print("listing_id = " + listing_id)                                              
            # print("title = " + title)                  
        except:
            try:
                div_i = 1    
                title = self.driver.find_element_by_xpath('//*[@id="listing-page-cart"]/div/div['+str(2+div_i)+']/div/h1')
                listing_id = title.get_attribute('data-listing-id')
                title = title.text
                # print("listing_id = " + listing_id)
                # print("title = " + title)                  
            except:
                print("Failed to get title with url = " + url)            
        try:     
            cost = self.driver.find_element_by_xpath('//*[@id="listing-page-cart"]/div/div['+str(3+div_i)+']/div/div/div[1]/p').text
        except:
            cost = ""
        if "Price:" in cost:
            cost = cost[6:]

        # print("cost = " + cost)
        try:
            description = self.driver.find_element_by_xpath('//*[@id="wt-content-toggle-product-details-read-more"]/p').text
        except:
            description = ""
        # print("description = " + description)
        try:
            date = self.driver.find_element_by_xpath('//*[@id="content"]/div[1]/div[2]/div[3]/div[1]/div[1]').text[10:]
            # print("date = " + date)
        except:
            date = self.driver.find_element_by_xpath('//*[@id="content"]/div[2]/div[2]/div[3]/div[1]/div[1]').text[10:]
            # print("date = " + date)
        
        try:
            seller = self.driver.find_element_by_xpath('//*[@id="desktop_shop_owners_parent"]/div/div/div[2]/p[1]').text
        except:
            seller = ""
        # print("seller = " + seller)               


        df.loc[df_i] = [search_term, listing_id, title, cost, description, date, seller]

    def get_search_results(self, num_pages, search_term):
        self.driver.get(self.base_url)

        # lets insert into the search feild
        search_input = self.driver.find_element_by_id("global-enhancements-search-query")
        search_input.send_keys(search_term)
        search_submit = self.driver.find_element_by_xpath('//*[@id="gnav-search"]/div/div[1]/button') 
        search_submit.click()

        # now lets get the listings from this page!
        url_list = []
        for num_page in range(num_pages):
            # lets first see the number of results
            item_count = len(self.driver.find_elements_by_xpath('//*[@id="content"]/div/div[1]/div/div/div[3]/div[2]/div[4]/div/div[1]/div/li'))
            for i in range(item_count):
                url = ""
                try:
                    url = self.driver.find_element_by_xpath('//*[@id="content"]/div/div[1]/div/div/div[3]/div[2]/div[4]/div/div[1]/div/li['+str(i+1)+']/div/a').get_attribute('href')
                except:                                     
                    try:
                        url = self.driver.find_element_by_xpath('//*[@id="content"]/div/div[1]/div/div/div[3]/div[2]/div[4]/div/div[1]/div/li['+str(i+1)+']/div/div/a').get_attribute('href')
                    except:
                        print("didnt find!! with i = " + str(i+1))
                        continue
                url_list.append(url)
            
            self.driver.get("https://www.etsy.com/ca/search?q=upcycled+furniture&ref=pagination&page=" + str(num_page + 2)) 
            time.sleep(3)
         
        print("Found " + str(len(url_list)) + " url's to scrape for " + search_term)
        # print(url_list)

        # now lets go to each listing and grab its information
        df_listings = pd.DataFrame(columns = ['search_term', 'listing_id', 'listing_title','listing_cost', 'listing_description', 'listing_date', 'listing_seller']) 
        df_listings_i = 1

        for url in url_list:
            self.get_listing_info(search_term, url, df_listings, df_listings_i)
            df_listings_i = df_listings_i + 1

        
        # df_listings.to_csv("test.csv", index=False)
        return df_listings


scraper = etsy()


#### use these lists and the funciton bellow to create a list of word combinations! ###
# listA = ["upcycled", "repurposed", "recycled"]
# listB = ["furniture", "jewelry", "accessories", "antiques", "décor", "home", "present(s)", "gift(s)"]
# word_list_temp = scraper.get_combinations(listA, listB)

# lets get the run_type 
print("Hi beatiful person! To continue please enter one of the folowing options:")
print("    - Please enter 1 to run for a term!")
print("    - Please enter 2 to run for a list of terms in a csv file!")

run_type = input("option: ")
# lets get the output file name
output_filename = input("Please enter a output file name: ")


if run_type == "1":
    search_term = input("please enter a search term: ")
    # need to process term
    output = scraper.get_search_results(10, search_term)
    output.to_csv(output_filename, index=False)
    print("Done! Have a great day! :)")

elif run_type == "2":
    # lets load the input file! 
    input_filename = input("please enter name of input file: ")
    try:
        term_list_temp = pd.read_csv(input_filename)
    except:
        print("Input file name was not valid! Please enter a valid input file name and make sure the file is in the same folder as this script!")
        exit()
    term_list_temp = term_list_temp.search_term.unique()

    # lets see if the output exists
    if not os.path.exists(output_filename):
        # if it doesnt then lets make it!
        temp = pd.DataFrame(columns = ['search_term', 'listing_id', 'listing_title','listing_cost', 'listing_description', 'listing_date', 'listing_seller']) 
        temp.to_csv(output_filename , mode='w', header=True, index=False)
        done_terms = []
    else:    
        done_terms = pd.read_csv(output_filename)
        done_terms = done_terms.search_term.unique()
    
    # lets remove any terms that are extra!
    term_list = []
    for i in term_list_temp: 
        if not i in done_terms:
            term_list.append(i)
    
    print("list of terms to process: ")
    print(term_list)

    # finally lets run for the terms left over!
    
    outputs = []
    for i in term_list:
        output = scraper.get_search_results(10, i)
        # outputs.append(output)
        output.to_csv(output_filename, mode='a', header=False, index=False)

    print("Done! Have a great day! :)")


#### THIS IS FOR TESTING ONLY ####
# url = "https://www.etsy.com/ca/listing/916524641/large-22-barn-beam-block-side-table?ga_order=most_relevant&ga_search_type=all&ga_view_type=gallery&ga_search_query=recycled+furniture&ref=sr_gallery-1-18&organic_search_click=1&frs=1"
# url = "https://www.etsy.com/ca/listing/958133357/barn-beam-sofa-tableshelf?ref=sold_out-4"
# scraper.get_listing_info("test", url, "", 1)
