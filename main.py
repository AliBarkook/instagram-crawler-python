
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


siteCarsUrl = 'https://www.instagram.com/accounts/login/'
username = 'ghost_sniper001'
password = 'Pashmak2'

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


# ? open chrome 
driver.get(siteCarsUrl)

sleep(2)


usernameInput = driver.find_element_by_xpath('//*[@id="loginForm"]/div/div[1]/div/label/input')
usernameInput.send_keys(username)

passwordInput = driver.find_element_by_xpath('//*[@id="loginForm"]/div/div[2]/div/label/input')
passwordInput.send_keys(password)



# ? click submit button to login
WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="loginForm"]/div/div[3]/button/div'))).click()


# entry_hashtag = input('enter hashtag: ')
entry_hashtag = 'یلدا'

sleep(5)

# ? fill search input
searchInput = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="react-root"]/section/nav/div[2]/div/div/div[2]/input')))
searchInput.send_keys('#' + entry_hashtag)

sleep(1)
# ? open first result
WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.CLASS_NAME, '-qQT3'))).click()

sleep(5)

posts = driver.find_elements_by_class_name('v1Nh3')

sleep(2)

accountList = []
print('getting accounts name ...')
for post in posts:
    # ? find post url
    postUrl = post.find_element_by_tag_name('a').get_attribute('href')

    # ? read cookie use selenium and set to request
    cookies = driver.get_cookies()
    session = requests.Session()
    for cookie in cookies:
        session.cookies.set(cookie['name'], cookie['value'])

    # ? request to get post page
    postResponse = session.get(postUrl)
    beauti_Post = BeautifulSoup(postResponse.text, 'html.parser')

    # ? find account name
    account_name = (str(beauti_Post.find_all('script')[15]).split('username')[1]).split('"')[2]

    # ? add account name to list
    accountList.append(account_name)

print(accountList)

# textFileDirectory = 'account_lists/account_name(hashtag:' + entry_hashtag + ').txt'

# ? store account list to text file
with open('account_lists/account_name.txt' , 'w') as f:
    for line in accountList:
        f.write(line)
        f.write('\n')