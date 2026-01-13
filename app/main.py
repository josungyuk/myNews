from typing import Union
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from app.modules.news.application.service import crawling_service as cs

app = FastAPI()

@app.get("/news", response_class=HTMLResponse)
def get_news():
    """
    Docstring for get_news
    """
    result = cs.get_news()
    title = result[0][0]["title"]
    content = result[0][0]["content"]

    # 결과 구조가 <tuple><tuple><dict>인데, 그 이유가 <언론사별><n번째 기사별><제목/내용> 이기 때문이다.
    # 그렇기에 이제 DB연결이 필요하다.
    
    return f"""
    <!doctype html>
    <html lang="en">
      <head>
        <meta charset="utf-8">
        <title>News</title>
        <style>
          body {{
            max-width: 900px;
            margin: 40px auto;
            font-family: Arial, sans-serif;
          }}
          .article {{
            white-space: pre-wrap;
            line-height: 1.7;
            font-size: 16px;
          }}
        </style>
      </head>
      <body>
        <h1>{title}</h1>
        <div class="article">{content}</div>
      </body>
    </html>
    """