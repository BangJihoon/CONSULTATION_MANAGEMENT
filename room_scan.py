import mysql1 as sql
from selenium.webdriver.common.keys import Keys
import requests
import time, os
import upload_image

def room_scan(driver):
    driver.switch_to_window(driver.window_handles[1])
    up_img = upload_image.Upload_image()

    # 상담자
    nickName = driver.find_element_by_xpath('//*[@id="kakaoWrap"]/div[1]/div[1]/div[1]/div/div/strong').text
    nickName = nickName.split('\n')[1].replace('/', '')

    # 채팅방 폴더 만들기
    save_url = './img/' + nickName + '/'
    if os.path.isdir(save_url) is False:
        os.mkdir(save_url)

    # 담당자
    chat_manager = driver.find_element_by_class_name('tit_profile').text

    top_chat = ""
    scroll_flag=True
    # 채팅방 스크롤 올리기
    while scroll_flag:
        # current_chat = 현재화면에 최상단 메세지
        current_chat = driver.find_element_by_class_name('item_chat').text

        # 스크롤
        element = driver.find_element_by_tag_name('body')
        element.click()
        element.send_keys(Keys.HOME)  # home키를 누르게 하여 스크롤 올림
        time.sleep(0.5)  # 웹 자원 대기를 위해 0.5초

        # 스크롤중 띄워진 첨부파일창 핸들링
        if len(driver.window_handles) == 3:
            print('window=====' + str(1) + 'handles======' + str(len(driver.window_handles)))
            driver.switch_to_window(driver.window_handles[2])  # 사진이 클릭 되었을 시 창 닫음
            driver.close()
            driver.switch_to_window(driver.window_handles[1])
            print('num ======= ' + str(1))

        # 이전에 저장된 top_chat 과 동일하면, while문 종료
        if current_chat == top_chat:  #
            scroll_flag = False

        # 최상단 메세지를 current_chat에 저장
        top_chat = current_chat

    days = driver.find_elements_by_xpath("//*[@id=\"room\"]/div/div")
    time.sleep(1)
    for day in days:
        chat_date = day.find_element_by_class_name("bg_line").text
        items = day.find_elements_by_class_name("item_chat")
        for item in items:
            chat_msg = item.find_element_by_class_name('set_chat').text

            # 시간 처리 (오래걸리므로 삭제)
            # chat_time = ''
            # try:
            #     chat_time = item.find_element_by_class_name('txt_time').text
            # except:
            #     pass

            # 이미지 처리
            img_url = ''
            if str(item.get_attribute("class")).find("item_save") != -1:

                # 이미지 url 가져오기
                img_url = item.find_element_by_class_name('link_pic').get_attribute('href')

                # 파일 이름 뜯어오기
                filename = img_url.split('/')[-1]

                # 이미지 데이터 받기
                r = requests.get(img_url, allow_redirects=True)

                # 로컬에 저장
                open(save_url + filename, 'wb').write(r.content)

                # 드라이브에 저장후 ID값 반환
                img_url = up_img.saveImage(filename, nickName)

            print("============================")
            print("chat Date :" + chat_date)
            print("nick Name :" + nickName)
            print("manager :" + chat_manager)
            print("message :" + chat_msg)
            # print("chat Time :" + chat_time)
            print("url :" + img_url)
            print("============================")
            sql.save_msg(str(nickName), chat_date, '', chat_manager, str(chat_msg), img_url)

    driver.close()
    return driver