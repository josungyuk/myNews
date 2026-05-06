from app.common.config import tag as ct

parameters = [
    (ct.NewsSource.YNA, ct.NewsType.ECONOMY, ct.news_organ_homepage[(ct.NewsSource.YNA)], ct.news_organ_type[ct.NewsSource.YNA][ct.NewsType.ECONOMY], ct.news_organ_content_tag[(ct.NewsSource.YNA)]),
    (ct.NewsSource.YTN, ct.NewsType.ECONOMY, ct.news_organ_homepage[(ct.NewsSource.YTN)], ct.news_organ_type[ct.NewsSource.YTN][ct.NewsType.ECONOMY], ct.news_organ_content_tag[(ct.NewsSource.YTN)]),
    (ct.NewsSource.BBC, ct.NewsType.ECONOMY, ct.news_organ_homepage[(ct.NewsSource.BBC)], ct.news_organ_type[ct.NewsSource.BBC][ct.NewsType.ECONOMY], ct.news_organ_content_tag[(ct.NewsSource.BBC)]),
    (ct.NewsSource.GUARDIAN, ct.NewsType.ECONOMY, ct.news_organ_homepage[(ct.NewsSource.GUARDIAN)], ct.news_organ_type[ct.NewsSource.GUARDIAN][ct.NewsType.ECONOMY], ct.news_organ_content_tag[(ct.NewsSource.GUARDIAN)]),
    (ct.NewsSource.NPR, ct.NewsType.ECONOMY, ct.news_organ_homepage[(ct.NewsSource.NPR)], ct.news_organ_type[ct.NewsSource.NPR][ct.NewsType.ECONOMY], ct.news_organ_content_tag[(ct.NewsSource.NPR)]),
    
    (ct.NewsSource.YNA, ct.NewsType.WORLD, ct.news_organ_homepage[(ct.NewsSource.YNA)], ct.news_organ_type[ct.NewsSource.YNA][ct.NewsType.WORLD], ct.news_organ_content_tag[(ct.NewsSource.YNA)]),
    (ct.NewsSource.YTN, ct.NewsType.WORLD, ct.news_organ_homepage[(ct.NewsSource.YTN)], ct.news_organ_type[ct.NewsSource.YTN][ct.NewsType.WORLD], ct.news_organ_content_tag[(ct.NewsSource.YTN)]),
    (ct.NewsSource.BBC, ct.NewsType.WORLD, ct.news_organ_homepage[(ct.NewsSource.BBC)], ct.news_organ_type[ct.NewsSource.BBC][ct.NewsType.WORLD], ct.news_organ_content_tag[(ct.NewsSource.BBC)]),
    (ct.NewsSource.GUARDIAN, ct.NewsType.WORLD, ct.news_organ_homepage[(ct.NewsSource.GUARDIAN)], ct.news_organ_type[ct.NewsSource.GUARDIAN][ct.NewsType.WORLD], ct.news_organ_content_tag[(ct.NewsSource.GUARDIAN)]),
    (ct.NewsSource.NPR, ct.NewsType.WORLD, ct.news_organ_homepage[(ct.NewsSource.NPR)], ct.news_organ_type[ct.NewsSource.NPR][ct.NewsType.WORLD], ct.news_organ_content_tag[(ct.NewsSource.NPR)]),
]