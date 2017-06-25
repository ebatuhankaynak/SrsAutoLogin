from splinter import Browser
from time import sleep
import imaplib

def get_mails(mail_address, mail_pass):
    mail = imaplib.IMAP4_SSL('mail.bilkent.edu.tr')
    mail.login(mail_address, mail_pass)
    mail.list()
    mail.select("inbox")
    result, data = mail.search(None, "ALL")

    ids = data[0]
    id_list = ids.split()
    latest_email_id = id_list[-1]

    result, data = mail.fetch(latest_email_id, "(RFC822)")

    raw_email = data[0][1]
    return raw_email

def get_verification_code(raw_email):
    index = raw_email.find("Code: ")
    index += 6
    return raw_email[index : index + 5]

def begin_login(bilkent_id, password, mail, mail_pass):
    browser = Browser()
    browser.visit('https://stars.bilkent.edu.tr/srs/')

    input_elements = browser.find_by_tag('input')

    pass_field = input_elements[2]
    pass_id = pass_field['id']
    browser.execute_script("var y = document.getElementById(\"LoginForm_password\").type = \"password\"")

    browser.fill('LoginForm[username]', bilkent_id)

    browser.type(pass_field['name'], password)
    browser.find_by_name('yt0').click()

    sleep(1)

    raw_email = get_mails(mail, mail_pass)
    verification_code = get_verification_code(raw_email.decode("utf-8"))

    browser.fill("EmailVerifyForm[verifyCode]", verification_code)
    browser.find_by_name('yt0').click()

    sleep(1)
