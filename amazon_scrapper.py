from bs4 import BeautifulSoup
import requests
import smtplib
import time

header = {"User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36'}

url = input('Enter the url : ')

'''
url = 'https://www.amazon.in/Razer-DeathAdder-Essential-White-RZ01-03850200-R3M1/dp/B092R71V77/ref=rvi_sccl_7/262-6950954-8135513?pd_rd_w=Z70dn&content-id=amzn1.sym.59eebe5b-59e3-4882-b364-90a7b22774a2&pf_rd_p=59eebe5b-59e3-4882-b364-90a7b22774a2&pf_rd_r=FZJASCRFCFZMS0NCEE45&pd_rd_wg=EcwWb&pd_rd_r=4e1d7be5-74bb-4998-bfb7-d2ab91537b39&pd_rd_i=B092R71V77&th=1'
'''

def scrape():
    global product_title
    global product_price
    global alert_price
    global alert_mail
    global url

    html_page = requests.get(url,headers=header)

    soup = BeautifulSoup(html_page.content,'lxml')

    product_title = soup.find('span',class_="a-size-large product-title-word-break").text.strip()

    int_price = soup.find('span',class_="a-price-whole").text.strip()
    price = int_price[:-1].replace(',', '')

    product_price = int(price)

    print('')
    print(f"Product Name : {product_title}\n")
    print(f"The current price of the product is : ₹{product_price}\n")
    alert_price = int(input("Set the alert price : ₹"))
    if alert_price > product_price:
        print("\nYour alert price is higher than the current price !\n")
    alert_mail = input("\nEnter mail-id for price alert : ")
#    if '@' not in alert_mail:
#        print("Enter a valid email-id !")


def sendAlert():
    server = smtplib.SMTP("smtp.gmail.com",587)
    server.ehlo()
    server.starttls()
    server.ehlo()
    server.login('passgen.pybot@gmail.com','cjtnjyfzcbfzufyi')

    subject = f"The price has fallen by {product_price - alert_price} !"
    body = f"Product Name : {product_title}\n\nProduct Price : {alert_price}\n\nProduct Link : {url}\n"

    mail_content = f"Subject: {subject}\n\n{body}"

    server.sendmail(
        'passgen.pybot@gmail.com',
        alert_mail,
        mail_content
    )
    print("\nEmail sent!\n")
    server.quit()


scrape()

if alert_price < product_price:
    sendAlert()
else:
    print("\nYour price alert is set! You will recieve a mail if the price drops.\n")