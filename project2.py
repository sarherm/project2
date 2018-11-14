## SI 206 F18 - Project 2

## COMMENT HERE WITH:
## Your name: Sarah Herman  
## Anyone you worked with on this project and how you worked together: Sarah Fodor and Rachel Gordon 
## You can not share code, but can share ideas
###########

## Import statements
import unittest
import requests
import re
from urllib.request import urlopen
from bs4 import BeautifulSoup
import ssl

## PART 1  - Complete grab_headlines
## INPUT: soup - the soup object to process
## Grab the headlines from the "Most Read" section
## and return them in a list
def grab_headlines(soup):

    base_url = 'https://www.michigandaily.com/section/news'
    page = urlopen(base_url).read()
    
    soup = BeautifulSoup(page, "html.parser")
    
    # get the most read div
    top_read = soup.find_all('div', class_ = 'view view-most-read view-id-most_read view-display-id-panel_pane_1 view-dom-id-99658157999dd0ac5aa62c2b284dd266') 
    headlines = top_read[0].find_all('a')
    #headlines = top_read.find_all("li")
    
    # get the ordered list from that div
    list_headlines = []
    for headline in headlines: 
        list_headlines.append(headline.text)
    
    # get the links from the ordered list div

    # return the headlines
    return list_headlines
    #pass


## PART 2 Complete a function called get_headline_dict. It will take a soup object and return a dictionary
## with each story headline as a key and each story url as the value
## INPUT: soup - the soup object
## OUTPUT: Return - a dictionary with each story headline as the key and the story url as the value
def get_headline_dict(soup):
    
    # create the empty dictionary
    headline_dict = {}
    # get the story wrap divs
    story_wraps = soup.find_all('div', class_ = 'storywrap')

    
    # get the most read div
    #top_read = soup.find_all('div', class_ = "view view-most-read view-id-most_read view-display-id-panel_pane_1 view-dom-id-99658157999dd0ac5aa62c2b284dd266")
    for story in story_wraps: 
        # get the short headline
        short_headline = story.find('div', class_= 'views-field-field-short-headline').get_text()
        content = story.find('div', class_ = 'field-content')
        #find the link in headline div
        link = content.find('a')['href']
        # set the dictionary key to the headline and the url as the value
        headline_dict[short_headline.strip()] = link
    
    return headline_dict
      

## PART 3 Define a function called get_page_info. It will take a soup object for a story
## and return a tuple with the title, author, date, and the number of paragraphs
## in the body of the story
## INPUT: soup - the soup object
## OUTPUT: Return - a tuple with the title, author, date, and number of paragraphs
def get_page_info(soup):
    
    # get the title
    title = soup.find('div', class_ = 'pane-node-title').h2.get_text()
    # get the date
    date = soup.find('div', class_ = 'pane-node-created').find('div', class_ = 'pane-content').get_text()
    # get the author
    author = soup.find('div', class_ = 'byline').find('div', class_ = 'link').get_text().strip()
    # get the number of paragraphs
    num_paragraphs = len(soup.find('div', class_ = 'field-name-body').find_all('p'))
    # return the tuple
    return(title, date, author, num_paragraphs)
    

## Extra Credit
## INPUT: the dictionary that was returned from part 2
## OUTPUT: a new dictionary with just items that contain the word U-M or Ann Arbor
def find_mich_stuff(dict):
    new_dict = {}
    d_items = dict.items()
    for k, v in d_items: 
        if 'U-M' in k or 'Ann Arbor' in k:
            new_dict[k.strip()] = v
    return new_dict
    

########### TESTS; DO NOT CHANGE ANY CODE BELOW THIS LINE! ###########

def getSoupObjFromURL(url):
    """ return a soup object from the url """
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE

    html = urlopen(url, context=ctx).read()
    soup = BeautifulSoup(html, "html.parser")
    return soup

def getSoupObjFromFile(fileName):
    """ return a soup object from the file with the passed fileName"""
    file = open(fileName, 'r')
    text = file.read().strip()
    file.close()
    soup = BeautifulSoup(text, "html.parser")
    return soup

# testing on live urls - remove the string comments to run this 
'''
soup = getSoupObjFromURL("https://www.michigandaily.com/section/news")
# print(grab_headlines(soup))
# hDict = get_headline_dict(soup)
# print(hDict)
# # get page info for each story in hDict
# for key, value in hDict.items():
#     tuple = get_page_info(soup)
#     print(tuple)
# nDict = find_mich_stuff(hDict) # for extra credit
# print(nDict)
#hDict, "http://www.michigandaily.com/"
''' 

# Test using unittests and saved pages
class TestP2(unittest.TestCase):

    def setUp(self):
        self.soup = getSoupObjFromFile("news1.html")
        self.soup2 = getSoupObjFromFile("newsStory1.html")
        self.dict = get_headline_dict(self.soup)

    def test_grab_headlines(self):
        self.assertEqual(grab_headlines(self.soup),['Broken Record: Student survivor navigates painful reporting process', 'Assistant women’s gymnastics coach resigns after charge of obscene conduct with gymnast', 'Ann Arbor Pieology shuts down because of “unfortunate circumstances”', 'To the white men who told me that they “prefer” white women', 'Op-Ed: Why I declined to write a letter of recommendation  '])

    def test_get_headline_dict(self):
        dict = get_headline_dict(self.soup)
        url = dict['Dialogues on Diversity holds discussion on microaggressions, accountability']
        self.assertEqual(len(dict.items()), 19)
        self.assertEqual(url,'https://www.michigandaily.com/section/campus-life/diversity-sciences')

    def test_get_page_info(self):
        self.assertEqual(get_page_info(self.soup2), ('Panel discusses pros, cons of Library Lot ballot proposal', '\n    Thursday, October 25, 2018 - 9:28pm  ', 'Leah Graham', 17))

    
    def test_find_mich_stuff(self):
        dict = find_mich_stuff(self.dict)
        url1 = dict['Ann Arbor state Rep. proposes bill to vastly increase renewable energy']
        url2 = dict['U-M freshman runs for Ann Arbor School Board position']
        self.assertEqual(len(dict), 4)
        self.assertEqual(url1,'https://www.michigandaily.com/section/government/state-rep-proposes-bill-100-percent-renewable-energy-michigan-2050')
        self.assertEqual(url2,'https://www.michigandaily.com/section/ann-arbor/school-board-candidates-fight-name-recognition-race')
    

unittest.main(verbosity=2)
