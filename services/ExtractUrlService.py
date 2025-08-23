from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from models.company_name_histories import CompanyNameHistories
from models.upload_histories import UploadHistories
from models.black_lists import BlackLists
import time
import requests
from bs4 import BeautifulSoup
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from services.GoogleSearchService import GoogleSearchService
import csv
import datetime
from google import genai
from google.genai.types import Tool, GenerateContentConfig, GoogleSearch
import os
from flask import send_file


LIST_TEXT_CONTACT_JAPANESE = ["連絡先","お問い合わせ","メールアドレス","電話番号","住所","contact","contact us","資料請求","CONTACT","お問合せ","お問合せ窓口","出会いを大切に、個人を大切に。","WEBからのお申込はこちら","無料相談はこちら","contact_project","お問い合わせ","お問合せ","お問い合わせ","専門家にご相談ください。","お問い合わせ"]
LIST_TEXT_HREF = ["contact","contact-us ","contact_us","contactus","contact-us.html","contact_us.html","contactus",'contact-us',"#contact","contact_project","CONTACT US"]
LIST_DIV = ["contact-link","contact_banner","form-header","quote-form"]
LIST_NAME_INPUT = ["contact_mail_from","form-group","contact_banner"]
# LIST_TEXT_H_TAG = ["contact","contact-us ","contact_us","contactus","contact-us.html","contact_us.html","contactus","CONTACT"]
LIST_KEY_INPUT = ["company_name","department","name","furi_name","lastname","firstname","lastname_kana","firstname_kana","email","confirm_email","company_url","number_of_employees","phone","phone1","phone2","phone3","fax","zip","zip1","zip2","province","city","address","title_question","text_area"]
LIST_TEXT_BUTTON_SUBMIT = ["送　信","確認画面へ","送信する","この内容で送信する","入力内容確認画面へ",]
BLACK_LIST=["seleo.co.jp"]
def get_black_list():
    black_list = BlackLists.query.all()
    black_list = [item.url for item in black_list]
    return black_list
def finding_class_name_of_input_content(soup,LIST_INPUT_NAME):
    class_name = ""
    for name in LIST_INPUT_NAME:
        for input in soup.find_all('textarea', attrs={'name': name}):
            class_name = input['name']
            return class_name
    # find textarea
    if class_name == "":
        for textarea in soup.find_all('textarea'):
            class_name = textarea['name']
            break
    return class_name
def process_word(word):
    # if first character is . remove it
    if word[0] == ".": word = word[1:]
    # if first character is not / add / 
    if word[0] != "/": word = "/" + word
    return word

def find_url_from_company_name(company_name,id):
    is_complete = False
    error_message = ""
    print(f"id",id)
    try:
        CompanyNameHistories.update_status(id, 1)
    except Exception as e:
        print(f"Error: {e}")
        pass
    # Using Google search to find url
    url = GoogleSearchService.search_company(company_name)
    if url == "Not found":
        try:
            CompanyNameHistories.update_status(id, 3, "Not found")
        except Exception as e:
            print(f"Error: {e}")
            pass
        return
    black_list = get_black_list()
    # check domain in black list
    domain = url.split("/")[2]
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-gpu')
    options.add_argument('--disable-software-rasterizer')
    options.add_argument('--remote-debugging-port=9222')
    # print(f'Come here')
    latestchromedriver = "/root/.wdm/drivers/chromedriver/linux64/114.0.5735.90/chromedriver-linux64/chromedriver"
    service = Service(latestchromedriver)
    # driver = webdriver.Chrome(options=options, service=service)
    # driver = webdriver.Chrome(options=options)
    # Insert data into database
    # split /abc after domain
    url_remake = url.split("/")[0] + "//" + url.split("/")[2]
    # print(f"url",url_remake)
    # Get content of url
    contact_url = "Not found"
    try:
        # html_content = requests.get(url, headers=headers,timeout=5)
        driver = webdriver.Chrome(options=options, service=service)
        # driver = webdriver.Chrome(options=options)
        driver.set_page_load_timeout(20)
        try:
            driver.get(url)
        except Exception as e:
            print(f"Error: {e}")
            driver.quit()
            CompanyNameHistories.update_status(id, 3, "Error when open url")
        WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
        time.sleep(2)
        html_content = driver.page_source
        # html_content = requests.get(url, headers=headers,timeout=5)
        driver.quit()
        data_extract = {
            "url": url,
            "contact_url": contact_url,
        }
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        # if error then continue to next url
        is_complete = False
        error_message = str(e)
        pass
    # using beatifulsoup to parse html content
    soup = BeautifulSoup(html_content, 'html.parser')
    # check if exist input classname exist in LIST_NAME_INPUT
    for input in soup.find_all('div', class_=LIST_NAME_INPUT):
        contact_url = url
        break
    # fin all text in tag h2 and h3 to find contact
    for h2 in soup.find_all('h2'):
        if any(text.lower() in h2.text.lower() for text in LIST_TEXT_CONTACT_JAPANESE):
            contact_url = url
            break
    for h1 in soup.find_all('h1'):
        if any(text.lower() in h1.text.lower() for text in LIST_TEXT_CONTACT_JAPANESE):
            contact_url = url
            break
    # find if element a has text contact in LIST_TEXT_CONTACT_JAPANESE or has href in LIST_TEXT_HREF
    for a in soup.find_all('a', href=True):
        if any(text.lower() in a['href'].lower() for text in LIST_TEXT_HREF) or any(text.lower() in a.text.lower() for text in LIST_TEXT_CONTACT_JAPANESE):
            contact_url = a['href']
            break
    if "http" not in contact_url and contact_url != "Not found":
        contact_url = url_remake + process_word(contact_url)
    data_extract["contact_url"] = contact_url
    # Update company url in database
    try:
        CompanyNameHistories.update_contact_url(id, contact_url)
    except Exception as e:
        print(f"Error: {e}")
        pass
    print(f"contact_url",contact_url)
    return data_extract

import random
import json

GOOGLE_API_KEY = [
    "AIzaSyAJfeZ8tDl5ouN9gb_e3wq2f-Pn_bDfJ_4",  # atpress-ne-jp
    "AIzaSyDnj3X9c8e7D8TNt6GxtCOQnOGtFzj700g",  # atpress
    # "AIzaSyC6jQfkEhQ2uc5OmSbO-KD8vYso35C1I2A",  # findmodel
    # "AIzaSyAhHsY1vO86NFB0CSzd5_eKyv-oym7IQuQ",  # socialwire
]

client = [genai.Client(api_key=_) for _ in GOOGLE_API_KEY]
import sqlite3
def search_and_get_top_url(company_name, address, cooporation_number):
    #sleep 1s
    time.sleep(random.uniform(0.5, 1.5))
    # Check if the result is cached
    conn = sqlite3.connect("search_cache.db")
    cursor = conn.cursor()
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS search_results (
            company_name TEXT,
            address TEXT,
            cooporation_number TEXT,
            search_response TEXT,
            PRIMARY KEY (company_name, address, cooporation_number)
        )
    """
    )
    cursor.execute(
        "SELECT search_response FROM search_results WHERE company_name=? AND address=? AND cooporation_number=?",
        (company_name, address, cooporation_number),
    )
    cached_result = cursor.fetchone()
    if cached_result:
        return json.loads(cached_result[0])
    
    model_id = "gemini-2.0-flash-exp"
    google_search_tool = Tool(google_search=GoogleSearch())
    prompt = (
        f"""
    この会社の問い合わせページを探してURLだけ教えて下さい。日本語のサイトである必要があります。
    会社名: {company_name}, 住所: {address}, 法人番号: {cooporation_number}"""
        + """
    出力するフォーマットは 
    {
        "urls": 
            [
                {"url": "https://example.com", "info": "Note about the URL"}
            ],
        "notes": "Additional notes",
        "confidence": 1.0 // 自信がない場合は、confidenceを0.0にしてください。
    }
    です。このフォーマット以外は禁止です。
    """
    )
    try:
        response = random.choice(client).models.generate_content(
            model=model_id,
            contents=[prompt],
            config=GenerateContentConfig(
                tools=[google_search_tool],
                response_modalities=["TEXT"],
            ),
        )
    except Exception as e:
        print(f"Error: {e}")
        raise e
    response_text = response.text.replace("```json", "").replace("```", "")
    response_json = json.loads(response_text)
    # Store the result in the database
    cursor.execute(
        "INSERT INTO search_results (company_name, address, cooporation_number, search_response) VALUES (?, ?, ?, ?)",
        (company_name, address, cooporation_number, json.dumps(response_json)),
    )
    conn.commit()
    conn.close()
    return response_json
def process_response_gemini(company_name, address, cooporation_number,file_path_result,is_last_record,id):
    top_url = search_and_get_top_url(company_name, address, cooporation_number)
    try:
        if not os.path.exists(file_path_result):
            os.makedirs(os.path.dirname(file_path_result), exist_ok=True)
            with open(file_path_result, mode='w', newline='', encoding='utf-8-sig') as file:
                file.write('\ufeff')  # Write BOM
                csv_writer = csv.writer(file)
                csv_writer.writerow(["Company Name", "Address", "Cooperation Number", "Confidence", "Notes", "URL", "Info"])
        with open(file_path_result, mode='a', newline='', encoding='utf-8-sig') as file:
            csv_writer = csv.writer(file)
            if top_url:
                confidence = top_url.get("confidence", 0.9)
                notes = top_url.get("notes", "").replace("\n", " ").replace("\r", " ")
                urls = top_url.get("urls", [])
                url = urls[0].get("url", "") if urls else ""
                info = (urls[0].get("info", "") if urls else "").replace("\n", " ").replace("\r", " ")
                csv_writer.writerow([company_name, address, cooporation_number, confidence, notes, url, info])
                print(f"[ok] Company: {company_name}")
                if is_last_record:
                    UploadHistories.update_status(id, 2)
            else:
                if is_last_record:
                    UploadHistories.update_status(id, 2)
                csv_writer.writerow(company_name, address, cooporation_number, + ["", "", "","Not found"])
                print(f"[ng] {company_name} no URL")
    except Exception as e:
        with open(file_path_result, mode='a', newline='', encoding='utf-8-sig') as file:
            csv_writer = csv.writer(file)
            csv_writer.writerow([company_name, address, cooporation_number, "", "", "", str(e)])
def find_url_from_company_name_v2(company_name, address, cooporation_number,file_path_result,is_last_record,id):
    # Check if the result is cached
    #random sleep 1s
    time.sleep(random.uniform(0.5,2))
    url = ''
    conn = sqlite3.connect("search_cache_ggsearch.db")
    cursor = conn.cursor()
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS search_google_results (
            company_name TEXT,
            address TEXT,
            cooporation_number TEXT,
            company_url TEXT,
            PRIMARY KEY (company_name, address, cooporation_number)
        )
    """
    )
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS search_google_count (
            search_date DATE,
            number_of_search INTEGER,
            PRIMARY KEY (search_date)
        )
    """
    )

    # get count number call google search success by date
    date_now = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=-8))).strftime("%Y-%m-%d")

    cursor.execute(
        "SELECT company_url FROM search_google_results WHERE company_name=? AND address=? AND cooporation_number=?",
        (company_name, address, cooporation_number),
    )
    cached_result = cursor.fetchone()
    if cached_result:
        url = cached_result[0]
    else:
         # get count number call google search success by date
        cursor.execute(
            "SELECT number_of_search FROM search_google_count WHERE search_date=?",
            (date_now,),
        )
        count = cursor.fetchone()
        # check if not exist then insert new record
        if not count:
            cursor.execute(
                "INSERT INTO search_google_count (search_date, number_of_search) VALUES (?, ?)",
                (date_now, 0),
            )
        else:
            count = count[0]
            print(f"count",count)
            if count >= 30000:
                conn.commit()
                conn.close()
                return 'LIMIT_SEARCH_BY_DAY'
        # Using Google search to find url
        url = GoogleSearchService.search_company(company_name)
        cursor.execute(
        "INSERT INTO search_google_results (company_name, address, cooporation_number, company_url) VALUES (?, ?, ?, ?)",
            (company_name, address, cooporation_number, url),
        )
        # count number call google search success by date
        cursor.execute(
                "UPDATE search_google_count SET number_of_search = number_of_search + 1 WHERE search_date=?",
                (date_now,),
        )
    conn.commit()
    conn.close()
    # process save file
    try:
        if not os.path.exists(file_path_result):
            os.makedirs(os.path.dirname(file_path_result), exist_ok=True)
            with open(file_path_result, mode='w', newline='', encoding='utf-8-sig') as file:
                file.write('\ufeff')  # Write BOM
                csv_writer = csv.writer(file)
                csv_writer.writerow(["Company Name", "Address", "Cooperation Number", "Confidence", "Notes", "URL", "Info"])
        with open(file_path_result, mode='a', newline='', encoding='utf-8-sig') as file:
            csv_writer = csv.writer(file)
            if url:
                confidence = 0.9
                notes = "Process by google search"
                url = url
                info = ""
                csv_writer.writerow([company_name, address, cooporation_number, confidence, notes, url, info])
                print(f"[ok] Company: {company_name}")
                if is_last_record:
                    UploadHistories.update_status(id, 2)
            else:
                if is_last_record:
                    UploadHistories.update_status(id, 2)
                csv_writer.writerow(company_name, address, cooporation_number, + ["", "", "","Not found"])
                print(f"[ng] {company_name} no URL")
    except Exception as e:
        with open(file_path_result, mode='a', newline='', encoding='utf-8-sig') as file:
            csv_writer = csv.writer(file)
            csv_writer.writerow([company_name, address, cooporation_number, "", "", "", str(e)])
    return url


    
# create function download csv file by id
def download_csv_by_id(id):
    upload_histories = UploadHistories.query.get(id)
    if upload_histories:
        file_path = upload_histories.file_path_result
        #change file to BOM format and exist 20250122160224 in file name
        if os.path.exists(file_path) and '20250122160224' in file_path:
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()
            with open(file_path, 'w', encoding='utf-8-sig') as file:
                file.write('\ufeff' + content)
        return send_file(file_path, as_attachment=True, download_name=os.path.basename(upload_histories.file_name), mimetype='text/csv')
    return None
