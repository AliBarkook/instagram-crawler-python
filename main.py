
# ! modules:

# ? improt selenium module
from pydoc import text
from sys import orig_argv
from turtle import onclick
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


# ? import time and speep module
from time import time, sleep

# ? improt request module for http request
import requests

# ? import Beautiful soup module for pars html
from bs4 import BeautifulSoup

# ? import tkinter module for UI
import tkinter as tk
from tkinter import * 
from tkinter.ttk import *

# ? import thrading module
import threading

# ! class
from classes.comment_class import Comment_Class
from classes.excel_class import Excel_Class

site_login_url = 'https://www.instagram.com/accounts/login/'
site_url = 'https://www.instagram.com/'
username = 'ghost_sniper001'
password = 'Pashmak2'

class Thread_Class (threading.Thread):
   def __init__(self, link):
      threading.Thread.__init__(self)
      self.link = link
   def run(self):
      return get_account_name(self.link)


# ? create and return chrome driver
def createChromeDriver():
    options = webdriver.ChromeOptions()
    options.add_argument('--disable-blink-features=AutomationControlled')
    options.add_argument("--disable-extensions")
    options.add_experimental_option('useAutomationExtension', False)
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_argument("--start-maximized")
    return webdriver.Chrome('chromedriver/chromedriver', options=options)


# ? create driver and fix it`s bug
driver = createChromeDriver()
driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")


# ? login to instagram
def login(login_btn, account_limit, post_limit):
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

    login_btn.destroy()

    # ? add hashtag input in menu
    hashtag_lable = Label(root, text='enter hsashtag')
    hashtag_lable.pack()
    hashtag_entry = Entry(root,width=10)
    hashtag_entry.pack()  
    comment_btn = tk.Button(root, text = 'search', bg='#46BB3C', fg='#ffffff', width=20, command=lambda m="": search_hashtag(hashtag_entry, account_limit, post_limit))
    comment_btn.pack(side = 'top', padx=8, pady=8)         


# ? search for hashtag
def search_hashtag(hashtag_entry, account_limit, post_limit):
    entry_hashtag = '#' + hashtag_entry.get()
    print('searching for hashtag')

    # ? fill search input
    searchInput = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="react-root"]/section/nav/div[2]/div/div/div[2]/input')))
    searchInput.send_keys('#' + entry_hashtag)

    sleep(1)
    # ? open first result
    WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.CLASS_NAME, '-qQT3'))).click()

    sleep(5)

    get_account_list(account_limit, post_limit)


# ? get link of accounts
def get_account_list(account_limit, post_limit):
    print('getting accounts name ...')
    posts = driver.find_elements_by_class_name('v1Nh3')

    sleep(2)

    accountList = []

    index = 1

    # ? get account names and sotre to text file
    for post in posts:
        # ? find post url
        postUrl = post.find_element_by_tag_name('a').get_attribute('href')

        # ? create instanve form thread class and pass link and row to it
        thread1 = Thread_Class(postUrl)

        # ? start thread
        thread1.start()

        # ? add account name to list
        accountList.append(thread1.run())


        # ? check for account limit
        if index == account_limit:
            break

        index+=1


    # ? store account list to text file
    with open('queue/account_name.txt' , 'w') as f:
        for line in accountList:
            f.write(line)
            f.write('\n')

    get_post_list(post_limit)


# ? get post of accounts
def get_post_list(post_limit):
    account_list_file = open('queue/account_name.txt', 'r')
    accountList = account_list_file.readlines()
    print('getting accounts post urls')


    post_links = []
    for account in accountList:

        # ? open account page with selenium
        driver.get(site_url + account.strip())

        post_list = driver.find_elements_by_class_name('v1Nh3')

        index = 1
        # ? find posts href
        for post in post_list:
            post_links.append(post.find_element_by_tag_name('a').get_attribute('href'))

            if index == post_limit:
                break
            index+=1
        

    # ? store post link list to text file
    with open('queue/post_link.txt' , 'w') as f:
        for line in post_links:
            f.write(line)
            f.write('\n')


    get_excel_directory()
    get_comments()
    

# ? get comments and store to excel
def get_comments(excel_directory_entry):

    # ? create excel file and worksheet
    excel = Excel_Class('excels/' + excel_directory_entry.get() + '.xlsx', 'comments')
    excel.initExcel()

    # ? read post links from text file queue
    post_list_file = open('queue/post_link.txt', 'r')
    post_list = post_list_file.readlines()

    row = 1
    for index, post in enumerate(post_list):
        print('getting post number ' + str(index))
        driver.get(post.strip())

        sleep(2)

        # ? get all comments
        comment_list = driver.find_elements_by_class_name('Mr508')

        # ? get account name
        comment_account = driver.find_element_by_class_name('ZIAjV').text

        # ? get comments info
        print('getting comments info')
        for comment in comment_list:

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
            excel.storeDataInExcel(row, 0, commentInstance)
            row = row + 1

    excel.closeExcel()
    exit_application()


# ? get excel file name from user
def get_excel_directory():
    # ? input for excel file directory number
    excel_directory_lable = Label(root, text='enter excel file name')
    excel_directory_lable.pack()
    excel_directory_entry = Entry(root,width=10)
    excel_directory_entry.pack()

    # ? create continue button
    continue_btn = tk.Button(root, text = 'continue', bg='#46BB3C', fg='#ffffff', width=20, command=lambda m="": get_comments(excel_directory_entry))
    continue_btn.pack(side = 'top', padx=8, pady=8)


# ? get acuount names in multi threading mode
def get_account_name(postUrl):
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

    return account_name

 
# ? close driver and tkinter panel then exit app
def exit_application():
    driver.close()
    root.destroy()

# ? main function: start app
def main():
    
    # ? store account and post limit
    account_limit = int(account_count_entry.get())
    post_limit = int(post_count_entry.get())


    # ? remove prevouse step lable, input and button
    continue_btn.destroy()
    account_count_lable.destroy()
    account_count_entry.destroy()
    post_count_lable.destroy()
    post_count_entry.destroy()

    # ? Create login and exit Button
    login_btn = tk.Button(root, text = 'login', bg='#46BB3C', fg='#ffffff', width=20, command=lambda m="": login(login_btn, account_limit, post_limit))
    close_btn = tk.Button(root, text = 'exit', bg='#F04438', fg='#ffffff', width=20, command=lambda m="": exit_application())
    
    # ? Set the position of button on the top of window.  
    login_btn.pack(side = 'top', padx=8, pady=8)   
    close_btn.pack(side = 'top', padx=16, pady=16)   
    
    root.mainloop()


# ? init tkinter panel
root = Tk()

# ? Open window having dimension 300x300
root.geometry('300x300')

# ? input for accounts number
account_count_lable = Label(root, text='enter number of accounts that you want crawl')
account_count_lable.pack()
account_count_entry = Entry(root,width=10)
account_count_entry.pack()

# ? input for posts number
post_count_lable = Label(root, text='enter number of posts that you want crawl')
post_count_lable.pack()
post_count_entry = Entry(root,width=10)
post_count_entry.pack()

# ? create continue button
continue_btn = tk.Button(root, text = 'continue', bg='#46BB3C', fg='#ffffff', width=20, command=lambda m="": main())
continue_btn.pack(side = 'top', padx=8, pady=8)

root.mainloop()


