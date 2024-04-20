from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import re
from datetime import datetime
from tqdm.auto import tqdm
import pymysql

# 크롬 드라이버 자동 Install
ChromeDriverManager().install()

browser = webdriver.Chrome()
path = './chromedriver' #크롬 드라이버 저장 경로
#Yes24 베스트 셀러를 1페이지에 120개씩 볼수 있도록 URL 설정
# browser.get('https://www.yes24.com/Product/Category/BestSeller?categoryNumber=001&pageNumber=1&pageSize=120') #URL로 이동
# #페이지가 로딩 될때까지 10초간 대기, 로딩이 완료되면 다음 코드 즉시 실행
# browser.implicitly_wait(time_to_wait=1000) 

# 데이터 베이스 연결

conn = pymysql.connect(
    host='localhost',  # 데이터베이스 서버 주소
    user='root',       # 데이터베이스 사용자 이름
    password='root',  # 데이터베이스 비밀번호
    db='YES24',       # 데이터베이스 이름
    charset='utf8mb4',
    cursorclass=pymysql.cursors.DictCursor
)

def sql_execute(sql, *args) :
    with conn.cursor() as cursor :
        cursor.execute(sql,*args)
        if 'select' in sql.lower() :
            return cursor.fetchall()
        conn.commit()
        
        
fail_list = []
sql = """
        INSERT INTO Books(title, author,publisher,publishing,rating,review, sales,price,ranking,ranking_weeks)
        VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
        """
for page_num in range(1,43) :
    print('페이지 번호 :',page_num)
    browser.get(f"https://www.yes24.com/Product/Category/BestSeller?categoryNumber=001&pageNumber={page_num}&pageSize=24") #URL로 이동
    #페이지가 로딩 될때까지 10초간 대기, 로딩이 완료되면 다음 코드 즉시 실행
    browser.implicitly_wait(time_to_wait=10) 
    book_list = browser.find_element(By.ID, 'yesBestList').find_elements(By.CLASS_NAME, 'itemUnit')
    for i in range(len(book_list)) :
        book_list[i].find_element(By.CLASS_NAME, 'gd_name').click() #제목 클릭하여 접속
        browser.implicitly_wait(time_to_wait=10) 
        try :
            title = browser.find_element(By.CLASS_NAME, 'gd_name').text # 제목
        except : 
            fail_list.append(i)
            continue
        try :
            author = browser.find_element(By.CLASS_NAME, 'gd_auth').text # 저자
        except : 
            fail_list.append(i)
            continue
        try :
            publisher = browser.find_element(By.CLASS_NAME, 'gd_pub').text #출판사
        except : 
            fail_list.append(i)
            continue
        try : 
            publishing = browser.find_element(By.CLASS_NAME, 'gd_date').text #출판일
            match = re.search(r'(\d+)년 (\d+)월 (\d+)일', publishing)
            if match :
                year, month, day = match.groups()
                date_data = datetime(int(year), int(month), int(day))
                publishing = date_data.strftime('%Y-%m-%d')
            else :
                date_data = datetime(int(9999), int(12), int(31))
                publishing = date_data.strftime('%Y-%m-%d')
        except : 
            fail_list.append(i)
            continue
        try :
            rating = browser.find_element(By.CLASS_NAME, 'gd_rating').find_element(By.CLASS_NAME,'yes_b').text # 평점
        except : 
            rating = '0.0'
        try :
            review = browser.find_element(By.CLASS_NAME, 'gd_reviewCount').find_element(By.CLASS_NAME, 'txC_blue').text.replace(',','')#리뷰수
        except : 
            review = '0'
        try :
            sales = browser.find_element(By.CLASS_NAME, 'gd_sellNum').text.split(' ')[2].replace(',','') #판매지수
        except : 
            sales = '0'
        try :
            price = browser.find_element(By.CLASS_NAME, 'nor_price').find_element(By.CLASS_NAME, 'yes_m').text.replace(',','') #가격
        except : 
            fail_list.append(i)
            continue
        try :
            ranking = browser.find_element(By.CLASS_NAME, 'gd_best_tp02').text.split(' | ')[0]
            ranking = ''.join(filter(str.isdigit,ranking))#국내 도서랭킹
        except : 
            fail_list.append(i)
            continue
        try :
            ranking_weeks = browser.find_element(By.CLASS_NAME, 'gd_best_tp02').text.split(' | ')[1] #국내 TOP 100
            ranking_weeks = ''.join(filter(str.isdigit,ranking_weeks))
        except : 
            ranking_weeks = '0'
        browser.back()
        browser.implicitly_wait(time_to_wait=10) 
        sql_execute(sql, (title, author, publisher, publishing, rating, review, sales, price, ranking, ranking_weeks))
        print('저장 정보 :',title, author, publisher, publishing, rating, review, sales, price, ranking, ranking_weeks)