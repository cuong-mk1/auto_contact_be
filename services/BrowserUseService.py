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
import re
from langchain_openai import ChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI
from browser_use import Agent,BrowserConfig, Browser

from pydantic import SecretStr
# from dotenv import load_dotenv
# import os
# load_dotenv()
import asyncio
# from pydantic import SecretStr
# llm = ChatOpenAI(model="gpt-4o-mini")
# import google.generativeai as genai
# GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
# genai.configure(api_key=GEMINI_API_KEY)
# llm = ChatGoogleGenerativeAI(model='gemini-2.0-flash-lite', api_key=SecretStr("AIzaSyCc697G2QV6Zd4B-wdRi8YTiD_QRRcvjvE")) # New key 
llm = ChatGoogleGenerativeAI(model='gemini-2.0-flash-lite', api_key=SecretStr("AIzaSyCDEuySqczFy1gG8HQ1vP7AHHvsXNOpouM")) # Old key

# llm = ChatOpenAI(base_url='https://api.deepseek.com/v1', model='deepseek-chat', api_key=SecretStr("sk-c24d265744ed4adb890f6f733fc64e07"))

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

def process_word(word):
    # if first character is . remove it
    if word[0] == ".": word = word[1:]
    # if first character is not / add / 
    if word[0] != "/": word = "/" + word
    return word

async def submit_form(url,data_send,setting,id):
    is_complete = False
    error_message = ""
    print(f"id",id)
    JobHistories.update_status(id, 1)

    # black_list = get_black_list()
    # # check domain in black list
    # domain = url.split("/")[2]
    # is_black_list = False
    # check if domain in black list
    # for black in black_list:
    #     if domain in black or black in domain:
    #         is_black_list = True
    #         error_message = "Domain in black list"
    # if is_black_list:
    #     JobHistories.update_status(id, 3, error_message)
    #     return False
    # contact_url=url
    # open contact_url by selenium
    if url != "Not found":
        # JobHistories.update_contact_url(id, contact_url)
        config = BrowserConfig(
            headless=True,
            disable_security=True,
            # chrome_instance_path='/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',  # macOS path
            # chrome_instance_path=chrome_driver_path,  # Linux path
        )
        browser = Browser(config=config)
        dataInput = data_send
        agent = Agent(
            task=f"""
            **Agent Role:** You are an expert automation agent focused on detecting and fully completing contact forms on websites.
            **Primary Goal:** On the page `{url}`, find the primary contact form and fill it out completely using the data from `{dataInput}`. Prioritize accuracy and filling *every* field that matches a key in `dataInput`, especially required fields.
            **Instructions:**
            IMPORTANT: 
                * SKIP FILL IF THE CONTACT FORM IS REQUIRED PAYMENT OR FEE WHEN SUBMIT SALES CONTACT FORM
                * SKIP FILL IF THE CONTACT FORM EXISTED WORD LIKE '入会、入会申込' ,'資料請求', '予約', '求人' or the same meaning in Japanese, which indicates that the contact form is for membership or subscription applications.

            - When accessing a contact form page, if you detect any text that includes phrases such as:
               * "If we determine your message to be a sales inquiry, you will be charged 5,500 yen (tax included)."
                * Or any sentence indicating that a fee will be charged if the message is considered a sales email,
            - then immediately skip this page without submitting the form and proceed to the next target and return fail.
                Detection criteria:
                * The text contains monetary amounts (e.g., "5,500円", "10,000円") along with keywords like "営業メール" (sales email), "料金" (fee), "支払い" (payment), "請求" (charge).
                * Any sentence that asks for payment or mentions a charge if the message is classified as advertising or sales.
            - If no such text is found, proceed to fill out and submit the contact form as usual.
            - SKIP if the browser to extract and examine all text fields from contact forms before displaying any of my contact data in content sections on Japanese pages related to comments, especially those containing '応援コメントをお寄せください！' or 'コメント' then RETURN ERROR.
            IMPORTANT: SKIP if the browser to extract and examine all text fields from contact forms before displaying any of my contact data in content sections on Japanese pages related to comments, especially those containing '応援コメントをお寄せください！' or 'コメント' then RETURN ERROR.
            1. **Black List:** If the domain `{url}` is in the black list, do not fill the form and return `ERROR: Domain in black list {{"contact_url": "LAST_URL_SEEN"}}`
            1. **Stay on Page:** Only work within the content of `{url}`. Do not navigate away, open new tabs, or use external pages.
            2. **Do NOT Click Any Links:** Avoid clicking any `<a>` tags or elements that navigate to other URLs—even if styled like buttons. Only interact with form inputs and the final submit button.
            3. **Form Detection:** Locate the main contact form in the main content area. Ignore any forms in the `<header>` or `<footer>`.
            4. **Required Fields:** Identify required fields using markers like `*`, `required`, `aria-required="true"`, or required-like label text. Prioritize these.
            5. **Field Matching:**
            - Match `dataInput` keys to field labels, names, or placeholders. Use synonyms if exact matches don’t exist.
            - Attempt to use *every* key-value pair in `dataInput` if a corresponding field is present.
            6. **Filling Fields:**
            - **Text/TextArea:** Insert the full value from `dataInput`. For message/content fields, enter the complete text.
            - **Checkbox/Radio:** Use only the actual `<input>` elements. **Do not click** associated `<label>`s, pseudo-elements, or descriptions.
            - **Select/Dropdowns:** Open the dropdown and select the **last available `<option>`**.
            7. **Pre-Submit Check:** Ensure all required fields and all fields mapped from `dataInput` are filled before proceeding.
            8. **Submit the Form:**
            - Locate a valid **submit button** within the form: `<button>`, `<input type="submit">`, or similar (but not `<a>` elements).
            - Look for clear submission labels: "Submit", "Send", "Confirm", "Register", "Apply", "送信", "確認", "登録", or if text contains `いますぐダウンロード` or `いますぐ申し込む`.
            - Use attributes or position to identify the most likely submit button.
            - **Avoid** all cancel/reset/back buttons, generic links, or anything unrelated to submission.
            - If a confirmation step appears, complete it fully.
            - only focus to submit the form, do not click any other links
            - try hard to find the submit button and click it
            10. **Error Handling:**
                - If validation fails, review the error messages.
                - Fix and refill any missing or incorrect fields based on `dataInput`.
                - Retry submission with the same intelligent logic.
            11. **Interaction Limit:** Complete everything within 20 actions (clicks, typing, selections). Stop immediately if limit is exceeded.
            **Output Rules:**
            - On success: return `OK {{"contact_url": "ACTUAL_URL_HERE"}}` where ACTUAL_URL_HERE is the final URL where the form was filled
            - On failure: return `ERROR: [理由] {{"contact_url": "LAST_URL_SEEN"}}` (例: フォームが見つかりませんでした)
            - If you exceed 20 steps: return `ERROR: タスクが20ステップを超えました {{"contact_url": "LAST_URL_SEEN"}}`
            - IMPORTANT: All error reasons must be translated into Japanese.

            **Input Data:**
            - `url`: http://www.w3schools.com/TAGs/att_a_target.asp  
            - `dataInput`: *(A JSON object containing key-value pairs for form fields)*

            """,
            llm=llm,
            browser=browser
            
        )
        history = None
        timeout = 50
        
        try:
            history = await run_agent_with_timeout(agent, timeout)
        except asyncio.TimeoutError:
            print(f"Agent execution timed out after {timeout} seconds")
            error_message = "Agent execution timed out after {timeout} seconds"
            status = {
                'is_done': False,
                'steps_completed': [],
                'current_step': None,
                'error': error_message,
                'progress': None
            }
            JobHistories.update_status(id, 3, error_message)
            await browser.close()
            print(f"status",status)
            return False
        # Get detailed status information
        #save data history into file txt
        # with open(f'history_{id}.txt', 'w',encoding='utf-8') as f:
        #     f.write(str(history))
        print(f"history",history.extracted_content())

        status = {
            'is_done': history.is_done(),
            'final_result' : history.final_result(),
            'steps_completed': history.get_completed_steps() if hasattr(history, 'get_completed_steps') else [],
            'current_step': history.get_current_step() if hasattr(history, 'get_current_step') else None,
            'error': history.get_error() if hasattr(history, 'get_error') else None,
            'progress': history.get_progress() if hasattr(history, 'get_progress') else None, 
            'contact_url': history.get_contact_url() if hasattr(history, 'get_contact_url') else None
        }
        # Get contact_url in final_result
        final_result = history.final_result()
        contact_url = final_result
        #find ERROR: in final_result
        if (final_result and "ERROR:" in final_result.upper()) or final_result is None:
            is_complete = False
            error_message = final_result
        else:
            is_complete = True
            JobHistories.update_contact_url(id, contact_url)
        print(f"status",status)
    if is_complete:
        JobHistories.update_status(id, 2)
    else:
        JobHistories.update_status(id, 3, error_message)
    await browser.close()
    return is_complete
async def run_agent_with_timeout(agent, timeout):
    try:
        return await asyncio.wait_for(agent.run(), timeout=timeout)
    except asyncio.TimeoutError:
        print(f"Agent execution timed out after {timeout} seconds")
        return None
