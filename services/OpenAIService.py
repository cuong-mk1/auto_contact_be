from openai import OpenAI
import json
import re
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time
import requests
from bs4 import BeautifulSoup
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import os
from dotenv import load_dotenv
import google.generativeai as genai
GOOGLE_API_KEY="AIzaSyAJfeZ8tDl5ouN9gb_e3wq2f-Pn_bDfJ_4"
genai.configure(api_key=GOOGLE_API_KEY)
gemini_client = genai.GenerativeModel("gemini-2.0-flash-exp")

load_dotenv()
CHAT_GPT_KEY=os.getenv('CHAT_GPT_KEY')
client = OpenAI(
    api_key=CHAT_GPT_KEY,
)

class OpenAIService: 
    @staticmethod
    def test_openai(url):
            print(f'Come here',url)
            LIST_KEY_INPUT = ["company_name","department","name","furi_name","lastname","firstname","lastname_kana","firstname_kana","email","confirm_email","company_url","number_of_employees","phone","phone1","phone2","phone3","fax","zip","zip1","zip2","province","city","address","title_question","content_question"]
            options = Options()
            # options.add_argument('--headless')
            options.add_argument('--no-sandbox')
            options.add_argument('--disable-dev-shm-usage')
            options.add_argument('--disable-gpu')
            options.add_argument('--disable-software-rasterizer')
            options.add_argument('--remote-debugging-port=9222')
            # print(f'Come here')
            latestchromedriver = "/root/.wdm/drivers/chromedriver/linux64/114.0.5735.90/chromedriver-linux64/chromedriver"
            service = Service(latestchromedriver)
             # driver = webdriver.Chrome(options=options, service=service)
            driver = webdriver.Chrome(options=options)
            driver.set_page_load_timeout(30)
            driver.get(url)
            WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
            time.sleep(2)
            html_content = driver.page_source
            driver.quit()
            html = html_content
            tags_to_remove = ['link', 'style', 'script', 'footer', 'head', 'header']
            for tag in tags_to_remove:
                html = re.sub(rf'<{tag}[^>]*>[\s\S]*?</{tag}>', '', html)
            if '<form' in html:
                html = re.search(r'<form[^>]*>[\s\S]*?</form>', html).group()
            prompt = f"""
            You are an assistant specializing in analyzing HTML code to identify all input fields within a form. Below is an HTML snippet. Analyze it and provide the results in the following format:

            ### Requirements:
            1. Extract the class names of all input fields that accept user input.
            2. Identify mandatory fields based on attributes like `required` or other indicators within the form.
            3. Output the results in JSON format.
            4. Categorize input fields based on keys provided in `LIST_KEY_INPUT: {LIST_KEY_INPUT}`, and include this categorization in the JSON.

            ### Input:
            An HTML snippet provided in the variable `html`.

            ### Output:
            - **List of input fields** with key name is inputs: Include the `id`, `name`, description, input type, and corresponding key in `{LIST_KEY_INPUT}` for each input.
            - **Mandatory fields**: Highlight fields that are mandatory.

            ### Detailed Instructions:
            - Ensure all input fields in the form are listed, including both mandatory and optional ones.
            - For each input, provide:
            - `class_id`
            - `name`
            - Description of the input field
            - Input type (e.g., text, checkbox, radio, etc.)
            - Key from `{LIST_KEY_INPUT}`
            - Clearly indicate which fields are mandatory.
            - Format the entire output as JSON.
            - Categorize fields by keys in `LIST_KEY_INPUT`.
            - If there are multiple inputs for `phone` or `zip code`, label them as `phone1`, `phone2`, `phone3`, and `zip1`, `zip2`, etc.

            {html}
            """
            response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}]
            )
            print(f'Come here',response.choices[0].message.content.strip())
            data = response.choices[0].message.content.strip()
            # check if exist ```json the remove it and '```'
            if '```json' in data:
                data = re.sub(r'```json', '', data)
                data = re.sub(r'```', '', data)
            # convert to json
            data_json = json.loads(data)
            return data_json
    @staticmethod
    def get_inputs_form(html):
            LIST_KEY_INPUT = ["company_name","department","name","furi_name","lastname","firstname","lastname_kana","firstname_kana","email","confirm_email","company_url","number_of_employees","phone","phone1","phone2","phone3","fax","zip","zip1","zip2","province","city","address","title_question","content_question"]
            # remove all css and js and footer and head
            tags_to_remove = ['link', 'style', 'script', 'footer', 'head', 'header']
            for tag in tags_to_remove:
                html = re.sub(rf'<{tag}[^>]*>[\s\S]*?</{tag}>', '', html)
            # check if existed <form> tag only get form tag
            prompt = f"""
            You are an assistant specializing in analyzing HTML code to identify all input fields within a form. Below is an HTML snippet. Analyze it and provide the results in the following format:

            ### Requirements:
            1. Extract the class names of all input fields that accept user input.
            2. Identify mandatory fields based on attributes like `required` or other indicators within the form.
            3. Output the results in JSON format.
            4. Categorize input fields based on keys provided in `LIST_KEY_INPUT: {LIST_KEY_INPUT}`, and include this categorization in the JSON.

            ### Input:
            An HTML snippet provided in the variable `html`.

            ### Output:
            - **List of input fields** with key name is inputs: Include the `id`, `name`, description, input type, and corresponding key in `{LIST_KEY_INPUT}` for each input.
            - **Mandatory fields**: Highlight fields that are mandatory.

            ### Detailed Instructions:
            - Ensure all input fields in the form are listed, including both mandatory and optional ones.
            - For each input, provide:
            - `class_id`
            - `name`
            - Description of the input field
            - Input type (e.g., text, checkbox, radio, etc.)
            - Key from `{LIST_KEY_INPUT}`
            - Clearly indicate which fields are mandatory.
            - Format the entire output as JSON.
            - Categorize fields by keys in `LIST_KEY_INPUT`.
            - If there are multiple inputs for `phone` or `zip code`, label them as `phone1`, `phone2`, `phone3`, and `zip1`, `zip2`, etc.

            {html}
            """
            response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}]
            )
            data = response.choices[0].message.content.strip()
            # check if exist ```json the remove it and '```'
            if '```json' in data:
                data = re.sub(r'```json', '', data)
                data = re.sub(r'```', '', data)
            # convert to json
            data_json = json.loads(data)
            return data_json
    @staticmethod
    def get_inputs_form_4o(html):
            LIST_KEY_INPUT = ["company_name","department","name","furi_name","lastname","firstname","lastname_kana","firstname_kana","email","confirm_email","company_url","number_of_employees","phone","phone1","phone2","phone3","fax","zip","zip1","zip2","province","city","address","title_question","content_question"]
            # remove all css and js and footer and head
            tags_to_remove = ['link', 'style', 'script', 'footer', 'head', 'header']
            for tag in tags_to_remove:
                html = re.sub(rf'<{tag}[^>]*>[\s\S]*?</{tag}>', '', html)
            # check if existed <form> tag only get form tag
            prompt = f"""
            You are an assistant specializing in analyzing HTML code to identify all input fields within a form. Below is an HTML snippet. Analyze it and provide the results in the following format:

            ### Requirements:
            1. Extract the class names of all input fields that accept user input.
            2. Identify mandatory fields based on attributes like `required` or other indicators within the form.
            3. Output the results in JSON format.
            4. Categorize input fields based on keys provided in `LIST_KEY_INPUT: {LIST_KEY_INPUT}`, and include this categorization in the JSON.

            ### Input:
            An HTML snippet provided in the variable `html`.

            ### Output:
            - **List of input fields** with key name is inputs: Include the `id`, `name`, description, input type, and corresponding key in `{LIST_KEY_INPUT}` for each input.
            - **Mandatory fields**: Highlight fields that are mandatory.

            ### Detailed Instructions:
            - Ensure all input fields in the form are listed, including both mandatory and optional ones.
            - For each input, provide:
            - `class_id`
            - `name`
            - Description of the input field
            - Input type (e.g., text, checkbox, radio, etc.)
            - Key from `{LIST_KEY_INPUT}`
            - Clearly indicate which fields are mandatory.
            - Format the entire output as JSON.
            - Categorize fields by keys in `LIST_KEY_INPUT`.
            - If there are multiple inputs for `phone` or `zip code`, label them as `phone1`, `phone2`, `phone3`, and `zip1`, `zip2`, etc.
            - if only have one phone,your-phone, etc or zip code, it will be phone and zip

            {html}
            """
            response = client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": prompt}]
            )
            data = response.choices[0].message.content.strip()
            # check if exist ```json the remove it and '```'
            if '```json' in data:
                data = re.sub(r'```json', '', data)
                data = re.sub(r'```', '', data)
            # convert to json
            data_json = json.loads(data)
            return data_json
    @staticmethod
    def get_inputs_form_by_gemini(html):
            LIST_KEY_INPUT = ["company_name","department","name","furi_name","lastname","firstname","lastname_kana","firstname_kana","email","confirm_email","company_url","number_of_employees","phone","phone1","phone2","phone3","fax","zip","zip1","zip2","province","city","address","title_question","content_question"]
            # remove all css and js and footer and head
            tags_to_remove = ['link', 'style', 'script', 'footer', 'head', 'header']
            for tag in tags_to_remove:
                html = re.sub(rf'<{tag}[^>]*>[\s\S]*?</{tag}>', '', html)
            # check if existed <form> tag only get form tag
            prompt = f"""
            You are an assistant specializing in analyzing HTML code to identify all input fields within a form. Below is an HTML snippet. Analyze it and provide the results in the following format:

            ### Requirements:
            1. Extract the class names of all input fields that accept user input.
            2. Identify mandatory fields based on attributes like `required` or other indicators within the form.
            3. Output the results in JSON format.
            4. Categorize input fields based on keys provided in `LIST_KEY_INPUT: {LIST_KEY_INPUT}`, and include this categorization in the JSON.

            ### Input:
            An HTML snippet provided in the variable `html`.

            ### Output:
            - **List of input fields** with key name is inputs: Include the `id`, `name`, description, input type, and corresponding key in `{LIST_KEY_INPUT}` for each input.
            - **Mandatory fields**: Highlight fields that are mandatory.

            ### Detailed Instructions:
            - Ensure all input fields in the form are listed, including both mandatory and optional ones.
            - For each input, provide:
            - `class_id`
            - `name`
            - Description of the input field
            - Input type (e.g., text, checkbox, radio, etc.)
            - Key from `{LIST_KEY_INPUT}`
            - Clearly indicate which fields are mandatory.
            - Format the entire output as JSON.
            - Categorize fields by keys in `LIST_KEY_INPUT`.
            - If there are multiple inputs for `phone` or `zip code`, label them as `phone1`, `phone2`, `phone3`, and `zip1`, `zip2`, etc.

            {html}
            """
            response = gemini_client.generate_content(prompt)
            data = response.candidates[0].content.parts[0].text
            print("data",len(data))
            # check if exist ```json the remove it and '```'
            if '```json' in data:
                data = re.sub(r'```json', '', data)
                data = re.sub(r'```', '', data)
            # convert to json
            data_json = json.loads(data)
            return data_json
    # create function to check is business page using gemini from html content
    @staticmethod
    def check_business_page(html):
        prompt = f"""
            Analyze the following content and determine whether it contains warnings about using the contact form (お問い合わせフォーム) for business purposes. If it does, extract the relevant warning text and explain why this content may pose a risk when sending business-related information.

            Pay special attention to the following phrases, as they often appear in warnings from {html}:

                "営業目的で利用" (use for business purposes)
                "営業・勧誘" (sales, solicitation)
                "損害金" (penalty fee)
                "請求いたします" (will request payment)
                "法的措置" (legal action)
                "禁止事項" (prohibited items)
                "迷惑行為" (disruptive behavior)
                "当社の判断で" (at our company's discretion)
                "情報を公開" (will disclose information)
                "賠償責任" (liability for damages)
            ### Input:
                HTML text or extracted content from a contact form page (お問い合わせフォーム).
            ### Output:
                Warning detected: Yes or No
                Reason: Explanation of why the content is considered a warning
            ### Detailed Instructions:
                - Format the entire output as JSON. with key is_warning, reason
            """
        response = gemini_client.generate_content(prompt)
        data = response.candidates[0].content.parts[0].text
        print("data",len(data))
        # check if exist ```json the remove it and '```'
        if '```json' in data:
            data = re.sub(r'```json', '', data)
            data = re.sub(r'```', '', data)
        # convert to json
        data_json = json.loads(data)
        # Get json data
        return data_json
    


    

