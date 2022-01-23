
# ! modules:

# ? improt selenium module
from sys import orig_argv
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# ? improt request module for http request
import requests

# ? import Beautiful soup module for pars html
from bs4 import BeautifulSoup

# ! class
from classes.comment_class import Comment_Class
from classes.excel_class import Excel_Class

site_login_url = 'https://www.instagram.com/accounts/login/'
site_url = 'https://www.instagram.com/'
username = 'ghost_sniper001'
password = 'Pashmak2'


# ? create excel file and worksheet
# ? create instance from ecxel class
excel = Excel_Class('excels/comment_list.xlsx', 'comments')
excel.initExcel()

# ? create and return chrome driver
def createChromeDriver():
    options = webdriver.ChromeOptions()
    options.add_argument('--disable-blink-features=AutomationControlled')
    options.add_argument("--disable-extensions")
    options.add_experimental_option('useAutomationExtension', False)
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_argument("--start-maximized")
    # options.add_argument("incognito")
    return webdriver.Chrome('chromedriver/chromedriver', options=options)


# ? create driver and fix it`s bug
driver = createChromeDriver()
driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")

# entry_hashtag = input('enter hashtag: ')
entry_hashtag = 'یلدا'


# ? login to instagram
def login():
    print('trying to login')
    # ? open chrome 
    driver.get(site_login_url)

    sleep(2)

    # ? fill user and pass input
    usernameInput = driver.find_element_by_xpath('//*[@id="loginForm"]/div/div[1]/div/label/input')
    usernameInput.send_keys(username)

    passwordInput = driver.find_element_by_xpath('//*[@id="loginForm"]/div/div[2]/div/label/input')
    passwordInput.send_keys(password)

    # ? click submit button to login
    WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="loginForm"]/div/div[3]/button/div'))).click()

    sleep(5)        

# ? search for hashtag
def search_hashtag():
    print('searching for hashtag')

    # ? fill search input
    searchInput = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="react-root"]/section/nav/div[2]/div/div/div[2]/input')))
    searchInput.send_keys('#' + entry_hashtag)

    sleep(1)
    # ? open first result
    WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.CLASS_NAME, '-qQT3'))).click()

    sleep(5)

# ? get href of accounts
def get_account_list():
    print('getting accounts name ...')
    posts = driver.find_elements_by_class_name('v1Nh3')

    sleep(2)

    accountList = []

    for post in posts:
        # ? find post url
        postUrl = post.find_element_by_tag_name('a').get_attribute('href')

        # ? read cookie use selenium and set to request
        cookies = driver.get_cookies()
        session = requests.Session()
        for cookie in cookies:
            session.cookies.set(cookie['name'], cookie['value'])

        # ? request to get post account page
        postResponse = session.get(postUrl)
        beauti_Post = BeautifulSoup(postResponse.text, 'html.parser')

        # ? find account name
        account_name = (str(beauti_Post.find_all('script')[15]).split('username')[1]).split('"')[2]

        # ? add account name to list
        accountList.append(account_name)

    print(accountList)

    # ? store account list to text file
    with open('account_lists/account_name.txt' , 'w') as f:
        for line in accountList:
            f.write(line)
            f.write('\n')

# ? get post of accounts
def get_post_list():
    print('getting accounts post urls')
    accountList = ['marii.family', 'sam.product',]
    print(accountList)



    post_links = []
    for account in accountList:

        # ? open account page with selenium
        driver.get(site_url + account)

        post_list = driver.find_elements_by_class_name('v1Nh3')


        # ? find posts href
        for post in post_list:
            post_links.append(post.find_element_by_tag_name('a').get_attribute('href'))
        

        postResponse = session.get(site_url + account)
        beauti_Post = BeautifulSoup(postResponse.text, 'html.parser')

        with open('readme.txt' , 'w', encoding="utf-8") as f:
            f.write(str(beauti_Post.prettify()))

        print(beauti_Post.find_all(class_='v1Nh3 '))


    # ? store post link list to text file
    with open('account_lists/post_link.txt' , 'w') as f:
        for line in post_links:
            f.write(line)
            f.write('\n')

# ? get comments and store to excel
def get_comments():
    driver.get('https://www.instagram.com/p/CWvLWa_A2r3/')

    sleep(2)

    # ? get all comments
    comment_list = driver.find_elements_by_class_name('Mr508')

    # ? get account name
    comment_account = driver.find_element_by_class_name('ZIAjV').text

    # ? get comments info
    print('getting comments info')
    for index, comment in enumerate(comment_list):

        # ? crawle comment text, author, like count and account name
        comment_text = comment.find_elements_by_tag_name('span')[1].text
        comment_author_account = comment.find_element_by_class_name('sqdOP').text
        comment_like = comment.find_elements_by_class_name('FH9sR')[1].text
        if 'like' in comment_like:
            comment_like = comment_like[0]
        else:
            comment_like = '0'

        # ? create instance from comment class
        commentInstance = Comment_Class(comment_account, comment_text, comment_author_account, comment_like)
        # ? store course in excel
        excel.storeDataInExcel(index+1, 0, commentInstance)

login()
get_comments()
excel.closeExcel()