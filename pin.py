import glob
import time
from random import randint
from selenium import webdriver


# Your Pinterest account details
user_name = "YOUR_PINTEREST_USER_NAME"
user_password = "YOUR_PINTEREST_PASSWORD"


# Definitions about pins
image_file = "YOUR_IMAGE_FOLDER_PATH"
description = "YOUR PINS' DESCRIPTION"


# Definitions for Selenium, don't change them
driver = webdriver.Chrome('./chromedriver')
pinterest_home = "https://www.pinterest.com/"
pre_login_button = '//*[@id="__PWS_ROOT__"]/div[1]/div/div/div/div[1]/div[1]/div[2]/div[2]/button'
login_button = "//button[@type='submit']"
pin_builder = "https://www.pinterest.com/pin-builder/"
pin_name = "//*[starts-with(@id, 'pin-draft-title-')]"
pin_description = "//*[starts-with(@id, 'pin-draft-description-')]/div/div/div/div/div/div/div"
image_input = "//*[starts-with(@id, 'media-upload-input-')]"
pin_link = "//*[starts-with(@id, 'pin-draft-link-')]"
drop_down_menu = "//button[@data-test-id='board-dropdown-select-button']"
publish_button = "//button[@data-test-id='board-dropdown-save-button']"





# Getting images from the file
image_list = []
for filename in glob.glob('images/*.jpg'):
    filename = filename[7:]
    image_list.append(filename)


# Getting links from the file
link_list = []
link_file = open("links.txt", "r")
for link in link_file:
    link = link.rstrip()
    link_list.append(link)


# Making link-image pairs
pairs = {}
for i in range(len(image_list)):
    pairs[image_list[i]] = link_list[i]



# Defining your Pinterest boards, keywords, link and tags
board_data = {"board_category_1": {
                        "keywords": ["KEYWORD1", "KEYWORD2", "KEYWORD3", "KEYWORD4", "KEYWORD5"],
                        "link": "//*[@title='YOUR_PINTEREST_BOARD_NAME']",
                        "tags": "#HASHTAG1 #HASHTAG2 #HASHTAG3 #HASHTAG4 #HASHTAG5 #HASHTAG6"},
                "board_category_2": {
                        "keywords": ["KEYWORD1", "KEYWORD2", "KEYWORD3", "KEYWORD4", "KEYWORD5", "KEYWORD6", "KEYWORD7", "KEYWORD8" ],
                        "link": "//*[@title='YOUR_PINTEREST_BOARD_NAME']",
                        "tags": "#HASHTAG1 #HASHTAG2 #HASHTAG3 #HASHTAG4 #HASHTAG5"},
                "example_category_tech": {
                        "keywords": ["LAPTOP", "TECHNOLOGY", "COMPUTER", "APPLE", "CANON", "CAMERA", "HEADPHONES", "SPEAKER", "KEYBOARD", "MOUSE PAD"],
                        "link": "//*[@title='Technology Accessories']",
                        "tags": "#tech #technology #accessories"},
                "example_category_food": {
                        "keywords": ["FOOD", "RECIPE", "CAKE", "PASTA", "SOUP", "BEEF", "CHICKEN", "SALAD", "DESERT", "BAKE"],
                        "link": "//*[@title='Tasty Recipes']",
                        "tags": "#food #recipe #cook #cooking #hungry"}
                }



# Slicing product name if you need. You can see the example below
# In the example we get the product name from "black_and_white_abstract_dots_pattern_baby_blanket-r38548522b52d4124bd270cf8060f89b3_jz0n5.jpg"
# After function pre_name will be  "BLACK AND WHITE ABSTRACT DOTS PATTERN BABY BLANKET"
# You can edit this section to get desired name
def pre_name():
    ind = img.find("-")
    product = img[:(ind)]
    pre_name = product.replace("_", " ")
    pre_name = pre_name.upper()
    return pre_name


# Defining link from image-link pair dictionary
def pre_link():
    pre_link = pairs[img]
    return pre_link


# Setting pinterest board and tags
def pre_board():
    general = "#blog #writing #tutorial "
    for i in board_data.keys() :
        for x in board_data[i]:
            for y in board_data[i]["keywords"]:
                if y in pre_name():
                    return (board_data[i]["link"], general + board_data[i]["tags"])


# Pinterest Log in
def login():
    # Open Pinterest on Chrome Driver
    driver.get(pinterest_home)
    time.sleep(20)

    # Click log in link
    driver.find_element_by_xpath(pre_login_button).click()
    time.sleep(20)

    # Log in
    user = driver.find_element_by_name("id")
    user.send_keys(user_name)
    time.sleep(10)
    pas = driver.find_element_by_name("password")
    pas.send_keys(user_password)
    time.sleep(10)
    driver.find_element_by_xpath(login_button).click()
    time.sleep(25)



def pin() :
    note = f'{description} {tags}'

    # Go pin builder page
    driver.get(pin_builder)
    time.sleep(10)

    # Click the upload button
    driver.find_element_by_xpath(image_input).send_keys(image_file + img)
    time.sleep(15)

    # Enter pin name
    driver.find_element_by_xpath(pin_name).send_keys(name.title())
    time.sleep(5)

    # Enter description
    driver.find_element_by_xpath(pin_description).send_keys(note)
    time.sleep(5)

    # Enter link
    driver.find_element_by_xpath(pin_link).send_keys(link)
    time.sleep(5)

    # Open board drop-down menu
    driver.find_element_by_xpath(drop_down_menu).click()
    time.sleep(10)

    # Select board
    driver.find_element_by_xpath(board).click()
    time.sleep(5)

    # Click publish button
    driver.find_element_by_xpath(publish_button).click()
    time.sleep(5)




# Pinning from file
login()
i = 0
while i < len(image_list):
    for img in image_list:
        name, board, tags, link = pre_name(), pre_board()[0], pre_board()[1], pre_link()
        pin()
        i += 1
        print(name.title(), "pinned on", board[12:-2])
        print(link)
        print("{} image(s) are pinned.".format(i))
        t = randint(10,100)
        print("Waiting next session...{} seconds \n".format(t))
        time.sleep(t)
print("All done! I've pinned {} images!".format(i))
driver.quit()
