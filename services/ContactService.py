from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from models.job_histories import JobHistories
from models.black_lists import BlackLists
import time
import requests
from bs4 import BeautifulSoup
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from services.OpenAIService import OpenAIService
import re

LIST_TEXT_CONTACT_JAPANESE = ["連絡先","お問い合わせ","メールアドレス","電話番号","住所","contact","contact us","資料請求","CONTACT","お問合せ","お問合せ窓口","出会いを大切に、個人を大切に。","WEBからのお申込はこちら","無料相談はこちら","contact_project","お問い合わせ","お問合せ","お問い合わせ","専門家にご相談ください。","お問い合わせ"]
LIST_TEXT_HREF = ["contact","contact-us ","contact_us","contactus","contact-us.html","contact_us.html","contactus",'contact-us',"#contact","contact_project","CONTACT US"]
LIST_DIV = ["contact-link","contact_banner","form-header","quote-form"]
LIST_NAME_INPUT = ["contact_mail_from","form-group","contact_banner"]
# LIST_TEXT_H_TAG = ["contact","contact-us ","contact_us","contactus","contact-us.html","contact_us.html","contactus","CONTACT"]
LIST_KEY_INPUT = ["company_name","department","name","furi_name","lastname","firstname","lastname_kana","firstname_kana","email","confirm_email","company_url","number_of_employees","phone","phone1","phone2","phone3","fax","zip","zip1","zip2","province","city","address","title_question","text_area"]
LIST_TEXT_BUTTON_SUBMIT = ["送　信","確認画面へ","送信する","この内容で送信する","入力内容確認画面へ","上記の同意して送信する"]

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

def submit_form(url,data_send,setting,id):
    is_complete = False
    error_message = ""
    print(f"id",id)
    try:
        JobHistories.update_status(id, 1)
    except Exception as e:
        print(f"Error: {e}")
        pass

    black_list = get_black_list()
    # check domain in black list
    domain = url.split("/")[2]
    is_black_list = False
    # check if domain in black list
    for black in black_list:
        if domain in black:
            is_black_list = True
            error_message = "Domain in black list"
    if is_black_list:
        # JobHistories.update_status(id, 3, error_message)
        return False
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        'Accept': '*/*',
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive'
    }
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
        driver.set_page_load_timeout(30)
        try:
            driver.get(url)
        except Exception as e:
            print(f"Error: {e}")
            driver.quit()
            JobHistories.update_status(id, 3, str(e))
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
        # if any(text in a.text for text in LIST_TEXT_CONTACT_JAPANESE):
        #     contact_url = a['href']
        #     break
    # check if not have http or https in contact_url then add domain to contact_url
    if "http" not in contact_url and contact_url != "Not found":
        contact_url = url_remake + process_word(contact_url)
    data_extract["contact_url"] = contact_url
    print(f"contact_url",contact_url)
    # open contact_url by selenium
    if contact_url != "Not found":
        JobHistories.update_contact_url(id, contact_url)
        try:
            # options = Options()
            # # options.add_argument('--headless')
            # options.add_argument('--no-sandbox')
            # options.add_argument('--disable-dev-shm-usage')
            # options.add_argument('--disable-gpu')
            # options.add_argument('--disable-software-rasterizer')
            # options.add_argument('--remote-debugging-port=9222')
            # print(f'Come here')
            # latestchromedriver = "/root/.wdm/drivers/chromedriver/linux64/114.0.5735.90/chromedriver-linux64/chromedriver"
            # service = Service(latestchromedriver)
            # driver = webdriver.Chrome(options=options, service=service)

            # driver = webdriver.Chrome(options=options)
            driver = webdriver.Chrome(options=options, service=service)

            try:
                driver.get(contact_url)
                time.sleep(3)
                # find <form> tag
                try:
                    form = driver.find_element(By.TAG_NAME, "form")
                except Exception as e:
                    form = None
                # check if not fond form then find iframe
                domain = contact_url.split("/")[2]
                if form is None:
                    iframe = WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((By.TAG_NAME, "iframe"))
                    )
                    if iframe:
                    # get data-src or src of iframe
                        iframe_src = iframe.get_attribute("data-src")
                        if iframe_src is None:
                            iframe_src = iframe.get_attribute("src")
                        print(f"iframe_src",iframe_src)
                        #extract domain from detail_url exclude http or https
                        if domain in iframe_src:
                            driver.switch_to.frame(iframe)
                        print(f"iframe_src",iframe_src) 
                # print(f"iframe",iframe)
                # Get html content of contact_url
                time.sleep(4)
                html_content = driver.page_source
                soup = BeautifulSoup(html_content, 'html.parser')
                # remove all css and js
                # find the input for name
                # list_inputs_form = OpenAIService.get_inputs_form(html_content)
                # check is blacklist from html content
                data = OpenAIService.check_business_page(html_content)
                is_black_list_url = data["is_warning"]
                reason = data["reason"]
                # check if is is_black_list_url then save to database and return
                if is_black_list_url:
                    #add into black list table
                    data_insert = {
                        "url": contact_url,
                        "reason": reason
                    }
                    BlackLists.create_data_black_lists(data_insert)
                    #save data to job_histories
                    JobHistories.update_status(id, 3, reason)
                    return False
                print(f"data",data)
                list_inputs_form = OpenAIService.get_inputs_form_by_gemini(html_content)

                print(f"inputs",list_inputs_form)
                #store input have sent key
                list_inputs_typed = []
                for input in list_inputs_form['inputs']:
                    key = input["key"]
                    input_name = input["name"]
                    input_id = input["class_id"]
                    print(f"key",key)
                    print(f"input_name",input_name)
                    print(f"input_id",input_id)
                    input_type = input["type"] if "type" in input else input["input_type"]
                    try:
                        if key == "name":
                            data_input = data_send["lastname"]  + data_send["firstname"]
                        elif key == "furi_name":
                            data_input = data_send["lastname_kana"] + data_send["firstname_kana"]
                        elif key == "phone1":
                            #get 3 first number of phone
                            data_input = data_send["phone"][:3]
                        elif key == "phone2":
                            #get 4 number of phone
                            data_input = data_send["phone"][3:7]
                        elif key == "phone3":
                            #get 4 number of phone
                            data_input = data_send["phone"][7:]
                        elif key == "confirm_email":
                            data_input = data_send["email"]
                        elif key == "text_area":
                            data_input = data_send["content_question"]
                        else:
                            data_input = data_send[key]
                        
                        if input_name != "":
                            try:
                                driver.find_element(By.NAME, input_name).send_keys(data_input)
                                list_inputs_typed.append(key)
                            except Exception as e:
                                driver.find_element(By.ID, input_id).send_keys(data_input)
                            time.sleep(2)
                    except Exception as e:
                        print(f"Error input name: {e}")
                        # if error then continue to next url
                        pass
                # click all radio
                try:
                    for radio in driver.find_elements(By.CSS_SELECTOR, "input[type='radio']"):
                        if radio.is_displayed() and radio.is_enabled():
                            radio.click()
                    time.sleep(2)
                except Exception as e:
                    print(f"Error click radio: {e}")
                    # if error then continue to next url
                    pass
                 # select first element of select input 
                try:
                    for select in driver.find_elements(By.CSS_SELECTOR, "select"):
                        select.click()
                        time.sleep(2)
                        for option in driver.find_elements(By.CSS_SELECTOR, "option"):
                            if option.is_displayed() and option.is_enabled():
                                option.click()
                except Exception as e:
                    print(f"Error click select: {e}")
                    # if error then continue to next url
                    pass
                try:
                    is_click = False
                    for checkbox in driver.find_elements(By.CSS_SELECTOR, "input[type='checkbox']"):
                        print(f"checkbox",checkbox)
                        if checkbox.is_displayed() and checkbox.is_enabled():
                            try:
                                # Wait until the checkbox is clickable
                                WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[type='checkbox']")))
                                # Use JavaScript to click the checkbox
                                driver.execute_script("arguments[0].click();", checkbox)
                                is_click = True
                            except Exception as e:
                                print(f"Error clicking checkbox: {e}")
                            is_click = True
                    print(f"is_click",is_click)
                    # if not click then fin text "の内容に同意します。" and click
                    if not is_click:
                        LIST_TEXT_CLICK_CONFIRM = ["の内容に同意します。",'を確認する','同意する']
                        for text in LIST_TEXT_CLICK_CONFIRM:
                            for label in driver.find_elements(By.CSS_SELECTOR, "label"):
                                if text in label.text:
                                    driver.execute_script("arguments[0].click();", label)
                                    break
                    time.sleep(2)
                except Exception as e:
                    print(f"Error click checkbox: {e}")
                    # if error then continue to next url
                    pass
                # click submit button
                print(f"list_inputs_typed",list_inputs_typed)
                if len(list_inputs_typed) == 0:
                    # check if not found input to type
                    is_complete = False
                    error_message = "Not found input to type"
                    JobHistories.update_status(id, 3, error_message)
                    driver.quit()
                    return False
                list_button_submit = []
                # find element by text in LIST_TEXT_BUTTON_SUBMIT
                for text in LIST_TEXT_BUTTON_SUBMIT:
                    elements = driver.find_elements(By.XPATH, f"//*[text()='{text}']")
                    # check if element is p tag then find parent
                    for element in elements:
                        if element.tag_name == "p":
                            element = element.find_element(By.XPATH, "..")
                            print(f"element",element.tag_name)
                            list_button_submit.append(element)
                    #     list_button_submit.extend(elements)
                    print(f"elements",elements)
                    list_button_submit.extend(elements)
                # Get input submit by type
                elements_input_submit = driver.find_elements(By.CSS_SELECTOR, "input[type='submit']")
                list_button_submit.extend(elements_input_submit)
                # Get button submit by type
                elements_button_submit = driver.find_elements(By.CSS_SELECTOR, "button[type='submit']")
                list_button_submit.extend(elements_button_submit)
                print(f"elements",elements)
                try:
                    # find button type submit and click
                     # Wait until the button is present and clickable
                    for button in list_button_submit:
                            try:
                                button.click()
                                print("clicked submit button")
                                time.sleep(4)
                                # check existed text submit complete
                                check_thankyou_url = check_thanks_url(driver.page_source,driver.current_url)
                                if check_thankyou_url:
                                    is_complete = True
                                    break
                                # Continue to click submit button if exist confirm
                                LIST_INPUT_NAME_CONFIRM = ["Submit","submit","送信","送信する","送信内容を確認する","確認","確認する","確認画面へ","確認画面に"]
                                list_button_confirm_submit = []
                                for text in LIST_INPUT_NAME_CONFIRM:
                                    element_confirm_by_name = driver.find_elements(By.CSS_SELECTOR, f"input[name={text}]")
                                    list_button_confirm_submit.extend(element_confirm_by_name)
                                element_confirm_by_type = driver.find_elements(By.CSS_SELECTOR, "input[type='submit']")
                                list_button_confirm_submit.extend(element_confirm_by_type)
                                for button in list_button_confirm_submit:
                                    button.click()
                                    is_complete = True
                                    print("clicked submit button confirm")
                                    time.sleep(2)
                                    break
                            except Exception as e:
                                print(f"Error click submit button: {e}")
                                # if error then continue to next url
                                continue
                    time.sleep(3)
                    is_complete = True
                    error_message = ""
                    JobHistories.update_status(id, 2)
                except Exception as e:
                    time.sleep(3)
                    print(f"Error click submit button: {e}")
                    # if error then continue to next url
                    # is_complete = False
                    # if "element click intercepted: Element <button" in str(e) and is_black_list == False:
                    #     error_message = ""
                    #     is_complete = True
                    error_message = str(e)
                    pass
                driver.quit()
            finally:
                driver.quit()
                pass
        except Exception as e:
            print(f"Error: {e}")
            # if error then continue to next url
            is_complete = False
            error_message = str(e)
            JobHistories.update_status(id, 3, error_message)
            # save data to database
    if is_complete:
        JobHistories.update_status(id, 2)
    else:
        JobHistories.update_status(id, 3, error_message)
    return is_complete
LIST_TEXT_COMPLETE = ["ありがとう","送信完了","完了しました", "処理が完了しました", "送信が成功しました","Thank you", "Submission complete", "Completed successfully", "Your request has been processed","処理完了", "送信成功","処理が完了", "送信が成功"]
LIST_TEXT_THANKS = ["thanks","thank-you","thankyou","complete","completed","ありがとう","送信完了"]
def check_thanks_url(source,url):
    soup = BeautifulSoup(source, 'html.parser')
    # check thanks in all text
    for text in LIST_TEXT_COMPLETE:
        if any(text.lower() in soup.text.lower() for text in LIST_TEXT_COMPLETE):
            return True
    # check if url existed LIST_TEXT_THANKS in url
    for text in LIST_TEXT_THANKS:
        if any(text.lower() in url.lower() for text in LIST_TEXT_THANKS):
            return True
    return False