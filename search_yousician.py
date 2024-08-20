import click
import requests
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException, TimeoutException, ElementClickInterceptedException


def main():
    try:
        print('Type 1 to use headless mode')
        print('Type 2 to use normal mode')
        mode = click.prompt('Choose mode,type 1 or 2, and press Enter')
        driver = choose_browser_regime(mode)
        get_full_search_results(driver)
    except Exception as e:
        print('Something went wrong', e)
        exit(1)


def choose_browser_regime(mode):
    """
    Function allows to run application with Chrome browser in headless mode
    """
    if mode=='1':
        chrome_options = Options()
        chrome_options.add_argument("--headless=new")
        driver = webdriver.Chrome(options=chrome_options)
    elif mode=='2':
        driver = webdriver.Chrome()
    else:
        print('invalid value, please try again')
        exit(1)
    return driver


def open_url(driver):
    """
    Function checks internet connection and opens Yousician search page
    """
    url = 'https://yousician.com/songs'
    if has_connection(url):
        driver.get(url)
    else:
        print("Check your internet connection and restart app")
        driver.quit()
        exit(1)


def make_search(driver):
    """
    Function performs search.
    The search query is entering from keyboard
    """

    #Open Yousician
    open_url(driver)
    wait_for_page_content_load(driver)

    #Manage bottom bar with cookies by tapping Accept button
    close_cookies_block(driver)

    #Work with search input and enter search query
    search_string = driver.find_element(By.CSS_SELECTOR, "input[class^='SearchInput']")
    search_string.clear()
    que = click.prompt('Please, type song name or author you want to find and press Enter')
    search_string.send_keys(que)
    search_string.send_keys(Keys.ENTER)
    print(f'Searching {que}')
    wait_for_page_content_load(driver)


def open_url(driver):
    """
    Open initial search page and checking internet connection
    """

    url = 'https://yousician.com/songs'
    if not has_connection(url):
        print("Check your internet connection")
        driver.quit()
        exit(1)
    else:
        driver.get(url)

def close_cookies_block(driver):
    """
    Function closes cookies bottom block clicking Accept all button
    """

    try:
        sleep(3)
        accept_button = WebDriverWait(driver, 10).until(
            lambda d: d.find_element(By.ID, "onetrust-accept-btn-handler"))
        accept_button.click()
        print('Cookies are accepted')
    except NoSuchElementException:
        print('Cookies bottom sheet has not appear')
    except TimeoutException:
        print('Cookies bottom sheet has not appeared within 10sec')
    except ElementClickInterceptedException:
        print('By the reason can not click on button')
    except Exception as e:
        print('Something went wrong', e)

def wait_for_page_content_load(driver, timeout=10):
    """
    Function checking that page load is completed fully
    """
    try:
        WebDriverWait(driver, timeout).until(
            lambda d: d.execute_script("return document.readyState") == "complete"
        )
    except Exception as e:
        print('Something went wrong, see details', e)
        exit(1)

def has_connection(url):
    """
    Function checks internet connection using requests library
    """

    try:
        requests.get(url, timeout=10)
        return True
    except (requests.ConnectionError, requests.Timeout) as e:
        return False
        exit(1)

def parse_song_and_artist_row(table_rows):
    """
    Extracts song and artist name from the table rows
    """
    try:
        song = table_rows.find_elements(By.CSS_SELECTOR, "p[class^='Typography']")[0].text
        artist = table_rows.find_elements(By.CSS_SELECTOR, "p[class^='Typography']")[1].text
        return song, artist
    except Exception as e:
        print(e)


def get_full_search_results(driver):
    """
    Collect all extracted data
    Handles multi page search result
    Sort result
    """
    make_search(driver)
    full_search = []
    is_pagination = False

    while True:
        wait_for_page_content_load(driver)

        table_rows = driver.find_elements(By.CSS_SELECTOR, "a[class^='TableHead']")
        for table_row in table_rows:
            search_row = parse_song_and_artist_row(table_row)
            if search_row:
                full_search.append(search_row)


        pagination = driver.find_elements(By.CSS_SELECTOR, "button[class^='PaginationButton']")

        if pagination and not is_pagination:
            print("More than one page found")
            is_pagination = True
            number = 2

        if not pagination or pagination[-1].get_attribute("disabled") is not None:
            if is_pagination:
                print("This is the last page")
            break
        print('go to page', number)
        pagination[-1].click()
        number = number+1

    if full_search==[]:
        print('Nothing found, try another time')
        driver.quit()
        exit(0)

    print('Sorting search result')
    sorted_results= sorted(full_search, key=lambda k: (k[1],k[0]))
    for song, artist in sorted_results:
        print(f'{artist} : {song}')



if __name__ == '__main__':
    main()
