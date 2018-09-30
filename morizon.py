from selenium import webdriver
import smtplib
from unidecode import unidecode
import pandas as pd
import time as t

driver = webdriver.Chrome('C:\Lingaro\Python\chromedriver_win32\chromedriver')

#const:

#wget_str = "cmd /c wget -P C:\Lingaro\#DREAL\Wget " + source


def open():
  driver.get ("https://www.morizon.pl/dzialki/otwocki/wiazowna/")
  driver.set_window_size(1920, 1080)
  #driver.find_element_by_name("username").send_keys("sobiczewski.ms.1")
  #driver.find_element_by_name ("password").send_keys("Muad79dib")
  #driver.find_element_by_xpath('//*[@id="loginForm"]/div[3]/a').click()
  
def set():
  driver.find_element_by_xpath('//*[@id="ps_living_area"]/div/span').click()
  size = driver.find_element_by_xpath('//*[@id="ps_living_area_from"]')
  size.send_keys(950)
  driver.find_element_by_xpath('//*[@id="ps_price"]/div/span/p').click()
  price = driver.find_element_by_xpath('//*[@id="ps_price_to"]')
  price.send_keys(500000)
  driver.find_element_by_xpath('//*[@id="ps"]/section[3]/input').click()

def search():
  msg = ''
  df = pd.DataFrame(columns=['#', 'TITLE', 'SUBTITLE', 'DESC', 'PRICE', 'LINK'])
  for i in range(1, 36):
    root = '//*[@id="contentPage"]/div/div/div/div/section/div[' + str(i) + ']/div/div/div/section'
    title = driver.find_element_by_xpath(root + '/header/a/div/div[1]/h2').text
    subtitle = driver.find_element_by_xpath(root + '/header/a/div/div[2]/p[2]').text
    desc = driver.find_element_by_xpath(root + '/div[1]/ul').text
    price = driver.find_element_by_xpath(root + '/header/a/div/div[2]/p[1]').text
    link = driver.find_element_by_xpath('//*[@id="contentPage"]/div/div/div/div/section/div[' + str(i) + ']/div/div/div/section/header/a').get_attribute('href')
    #print(f'{i:2}  {title:40}   {subtitle:20}   {desc:40}   {price:10}   {link:100}')
    #msg = msg + f'{i:2}  {title:40}   {subtitle:20}   {desc:40}   {price:10}   {link:100}' + '\n'
    df = df.append({'#': i, 'TITLE': title, 'SUBTITLE': subtitle, 'DESC': desc, 'PRICE': price, 'LINK': link}, ignore_index=True)
  return msg, df

def send(TO, msg_txt):
  #TO = 'sobiczewski.milosz@gmail.com'
  SUBJECT = 'Wiazowna - land on sale raport'
  TEXT = 'This message was send from python.'
  # Gmail Sign In
  gmail_sender = 'milosz.x.44@gmail.com'
  gmail_passwd = 'Atlas_L10'
  
  server = smtplib.SMTP('smtp.gmail.com', 587)
  server.ehlo()
  server.starttls()
  server.login(gmail_sender, gmail_passwd)
  
  msg_txt = unidecode(msg_txt)
  BODY = '\r\n'.join(['To: %s' % TO,
                      'From: %s' % gmail_sender,
                      'Subject: %s' % SUBJECT,
                      '', msg_txt + '\n' + TEXT])
  
  try:
      server.sendmail(gmail_sender, [TO], BODY)
      print ('email sent to ' + TO)
  except:
      print ('error sending mail')
  
  server.quit()

print ('Lets go:')
open()
print ('Site opened.')
set()
print ('Filters set.')
t.sleep(3)
#dac tu waita albo atempt 3 x
msg = search()
print ('Data search compleated.')
df = msg[1]
df2 = df['SUBTITLE'].str.split(' ', expand=True)
df3 = pd.concat([df, df2], axis=1, join_axes=[df.index])
df4 = df3.rename(index=str, columns={0: "val", 1: "unit"})
df5 = df4.sort_values(['val'], ascending=[0])
print (df5)
#send('sobiczewski.milosz@gmail.com', msg[0])
#send('katarzyna.sobiczewska@nethone.com', msg[0])
print ('End.')

#conn = MySQLdb.connect(host, user, password, database)
#cursor = conn.cursor()
#attempts = 0

#while attempts < 3:
#    try:
#        cursor.execute(query)
#        rows = cursor.fetchall()
#        for row in rows:
#            # do something with the data
#        break
#    except MySQLdb.Error, e:
#        attempts += 1
#        print "MySQL Error %d: %s" % (e.args[0], e.args[1])
#for attempt_number in range(3) 
