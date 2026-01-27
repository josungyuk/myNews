from app.modules.news.infra.crawling.sources import tag as ct

parameters = [
    (ct.NewsSource.YNA, ct.news_organ_homepage[(ct.NewsSource.YNA)], ct.news_organ_type[ct.NewsSource.YNA][ct.NewsType.ECONOMY], ct.news_organ_content_tag[(ct.NewsSource.YNA)]),
    (ct.NewsSource.YTN, ct.news_organ_homepage[(ct.NewsSource.YTN)], ct.news_organ_type[ct.NewsSource.YTN][ct.NewsType.ECONOMY], ct.news_organ_content_tag[(ct.NewsSource.YTN)]),
    (ct.NewsSource.BBC, ct.news_organ_homepage[(ct.NewsSource.BBC)], ct.news_organ_type[ct.NewsSource.BBC][ct.NewsType.ECONOMY], ct.news_organ_content_tag[(ct.NewsSource.BBC)]),
    # (ct.NewsSource.REUTERS, ct.news_organ_homepage[(ct.NewsSource.REUTERS)], ct.news_organ_type[ct.NewsSource.REUTERS][ct.NewsType.WORLDS][ct.Nomination.US], ct.news_organ_content_tag[(ct.NewsSource.REUTERS)]),
]