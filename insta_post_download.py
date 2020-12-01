from bs4 import BeautifulSoup
from selenium import webdriver 
import pickle
import time
import os
import urllib.request as utr

insta_link = 'https://www.instagram.com/'
def main_fun():
    print('Enter Instagram Id: ')
    username = input()
    create_folder(username)
    get_all_link(username)


def get_all_link(username):
    link = insta_link + username+'/'
    driver = webdriver.Chrome()
    driver.get(link)

    # To save your account login for next runs 
    #time.sleep(15)
    #with open('cookies.pkl', 'wb') as f:
    #    pickle.dump(driver.cookies, f)

    cookies = pickle.load(open("cookies.pkl", "rb"))
    for cookie in cookies:
        driver.add_cookie(cookie)
    driver.refresh()
    base = BeautifulSoup(driver.page_source,'html.parser')
    post_number = int(base.find('span',class_ = 'g47SY').get_text())
    print(f'Number of Post {post_number}')
    post_li_link = []
    for i in range(int(post_number/10)):
        driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
        soup = BeautifulSoup(driver.page_source,'html.parser')
        posts = soup.findAll('a')
        for post in posts:
            if '/p/' in post['href']:
                post_li_link.append(post['href'])
        time.sleep(1.5)
    get_all_post(username,driver,list(set(post_li_link)))


def get_all_post(username,driver,post_li_link):
    
    vi_counter = 0
    photo_counter = 0

    for lk in post_li_link:
        link = insta_link + lk
        driver.get(link)
        time.sleep(1)
        soup = BeautifulSoup(driver.page_source,'html.parser')
        images = soup.findAll('img')
        videos = soup.findAll('video')
        #print(images)

        for image in images:
            if image.has_key('srcset'):
                if image['srcset'].find('1080w') == -1 :
                    pass
                else:
                    x = image['srcset'].split(',')
                    for y in x:
                        if y.find('1080w') == -1 :
                            pass
                        else:
                            photo_counter += 1
                            download_image(username,y,photo_counter)
                            #print(y)
        for video in videos:
            if 'blob:'  not in video['src']:
                vi_counter += 1
                download_video(username,video['src'],vi_counter)
            


        
                    
def download_image(username,image_link,counter):
    file_name = username+'\\Photos\\'+ username +' ('+ str(counter) +').jpg'
    img_li = image_link.replace(' 1080w','')
    r = utr.urlopen(img_li)
    with open(file_name, "wb") as f:
        f.write(r.read())

def download_video(username,video_link,counter):
    file_name = username+'\\Videos\\'+ username +' ('+ str(counter) +').mp4'
    r = utr.urlopen(video_link)
    with open(file_name, "wb") as f:
        f.write(r.read())


def create_folder(username):
    check = os.path.isdir(username)

    # If folder doesn't exist, then create it.
    if not check:
        os.makedirs(username)
        video = username + '\Videos'
        photo = username + '\Photos'
        os.makedirs(video)
        os.makedirs(photo)
        print("created folder : ", username)

    else:
        print(username, "folder already exists.")


if __name__ == "__main__":
    main_fun()

