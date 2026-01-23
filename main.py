import requests
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright

url = "https://www.tiktok.com/@iamdeena_"

user_agent = f"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/144.0.0.0 Safari/537.36"

def crawling_by_playwright(url):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False, slow_mo=50)
        context = browser.new_context(user_agent=user_agent)
        page = context.new_page()
        page.goto(url)    
        content = page.content()

        input("Press Enter after the page is fully loaded...")

        # 팔로워 가져오기
        follower_element = page.locator('strong[title="팔로워"]')

        if follower_element.count() > 0:
            follower_text = follower_element.first.inner_text()
            print("팔로워(playwright):", follower_text)
        else:
            print("팔로워 정보를 찾을 수 없습니다.")
            print("다이나믹 페이지 이거나 봇 차단일 수 있습니다.")
        

        print(f"🚀{url} 크롤링 완료")

        browser.close()

def crawling_by_beautifulsoup(url):
    headers = {
        "User-Agent": user_agent
    }
    response = requests.get(url, headers=headers)

    # 응답 실패 처리
    if (response.status_code != 200):
        print(f"Error: {response.status_code}")
        return
    
    print(f"✅{url} 접속 성공")

    soup = BeautifulSoup(response.text, "html.parser")

    # __UNIVERSAL_DATA_FOR_REHYDRATION__ 찾기
    script_tag = soup.find("script", id="__UNIVERSAL_DATA_FOR_REHYDRATION__")
    
    if script_tag:
        print("✅__UNIVERSAL_DATA_FOR_REHYDRATION__ 스크립트 태그 발견")
        script_content = script_tag.text
        print(script_content)


    print(f"🚀{url} 크롤링 완료")

# crawling_by_playwright(url)
crawling_by_beautifulsoup(url)