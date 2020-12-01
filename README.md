# instagram-post-downloader
To download all post (photos and videos) from Instagram profile of your following or any public account.
1. install python into your system
2. install following packages
	* BeautifulSoup
	* selenium
	* pickle
3. Run python script and enter instagram id 
4. On 1st run we have to login into instagram 
   For 1st run Remove # from following line of script 

    # To save your account login for next runs 
    #time.sleep(15)
    #with open('cookies.pkl', 'wb') as f:
    #    pickle.dump(driver.cookies, f)

   Add # for following line
    cookies = pickle.load(open("cookies.pkl", "rb"))
    for cookie in cookies:
        driver.add_cookie(cookie)

5.Done from now you can run code and just enter user id and it will download all photos and videos in highest quality.

