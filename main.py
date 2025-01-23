import base64
from bs4 import BeautifulSoup
from newspaper import Article
import re
import os
from typing import List
from textrankr import TextRank
from konlpy.tag import Okt

# local 파일을 디코딩, html 파일로 저장 후 리턴하는 함수
def get_local_file():
    file_path = "news/article"
    with open(file_path,'rb') as f:
        decoded_art = base64.b64decode(f.read())
    with open("news/decoded_article.html",'wb') as ht:
        ht.write(decoded_art)
    with open("news/decoded_article.html", 'r', encoding='utf-8') as html:
        html_content = html.read()
    return html_content

# 특정 기사 url 로부터 기사 읽어오기, title 과 text 분리하는 함수
# 예: https://www.gamevu.co.kr/news/articleView.html?idxno=38226
def get_url_article(url):
    article = Article(url, language='ko')
    article.download()
    article.parse()
    # print(article.title)
    # print(article.text)
    return article.text

class MyTokenizer:
    def __call__(self, text):
        tokens = text.split()
        return tokens

def summarize_text(text: str) -> List[str]:
    summarized = textrank.summarize(text, 3)
    return summarized

## main 함수 선언
## 사용자의 입력을 받아, Local or 외부 url에 대해 기사를 읽어올 수 있게 선택
## 예) 요약할 기사의 출처를 선택하세요 > 1) local , 2) url
## 1. local 파일인 경우?
## 1-1. 파일명을 입력 받아 해당파일을 디코딩 > html 변경 후, 텍스트로 읽어오기
## 2. url 인 경우?
## 2-1. url 입력 받기
## 3. 입력받은 출처로부터 기사를 텍스트 형식으로 불러와서 요약
## 4. 요약된 내용을 local 파일 경로에 저장
## Bonus. 기사에 사용된 이미지를 불러와서, 요약된 기사에 이미지 넣기

if __name__ == "__main__":
    print('The News Extractor and Summarizer')
    print('1. Summarize Local File')
    print('2. Summrize Article from URL')
    print('3. Exit')
    choice = input('Enter your choice: ')
    choice = int(choice)
    if choice == 1:
        article = get_local_file()
    elif choice == 2:
        url = input('Enter the URL of the article: ')
        article = get_url_article(url)
    elif choice == 3:
        print('Exiting...')
        exit(0)
    try:
        mytokenizer = MyTokenizer()
        textrank = TextRank(mytokenizer)
        summarized_article = summarize_text(article)
        with open('news/summary_article.html','wb') as f:
            f.write(str(summarized_article).encode('utf-8'))
        print(summarized_article)
    except Exception as e:
        print(e)
        exit(1)
    