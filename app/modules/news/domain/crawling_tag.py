from enum import Enum

class NewsSource(Enum):
    YNA = "yna"
    YTN = "ytn"
    REUTERS = "reuters"
    BBC = "bbc"

class NewsType(Enum):
    ECONOMY = "economy"
    SOCIETY = "society"
    WORLDS = "worlds"

class Nomination(Enum):
    JAPAN = "japan"
    CHINA = "china"
    ASIA = "asia-pacific"
    UK = "uk"
    EU = "euroup"
    US = "us"
    AMERIA = "americas"
    ME = "middle-east"
    

news_organ_homepage = {
    NewsSource.YNA : "https://www.yna.co.kr",
    NewsSource.YTN : "https://www.ytn.co.kr",
    NewsSource.REUTERS : "https://www.reuters.com",
    NewsSource.BBC : "https://www.bbc.com"
}

news_organ_type = {
    NewsSource.YNA : {
        NewsType.ECONOMY : "economy/all",
        NewsType.SOCIETY : "society/all"
    },

    NewsSource.YTN : {
        NewsType.ECONOMY : "news/list.php?mcd=0102",
        NewsType.SOCIETY : "news/list.php?mcd=0103"
    },

    NewsSource.REUTERS : {
        NewsType.WORLDS : {
            Nomination.JAPAN : "world/japan",
            Nomination.CHINA : "world/china",
            Nomination.ASIA : "world/asia-pacific",
            Nomination.UK : "world/uk",
            Nomination.EU : "world/euroup",
            Nomination.US : "world/us",
            Nomination.AMERIA : "world/americas",
            Nomination.ME : "world/middle-east"
        }
    },

    NewsSource.BBC : {
        NewsType.ECONOMY : "business",
        NewsType.SOCIETY : "news/us-canada"
    }
}

news_organ_content_tag = {
    NewsSource.YNA : ".list01 a[href ^= 'https://www.yna.co.kr/view/']",
    NewsSource.YTN : ".title a[href ^= 'https://www.ytn.co.kr/_ln/']",
    NewsSource.REUTERS : ".TitleLink a[href ^= '/worlds/']",
    NewsSource.BBC : "a[href ^= '/news/articles/']"
}

new_organ_extract_title_tag = {
    NewsSource.YNA : "h1.tit01",
    NewsSource.YTN : "h2.news_title",
    NewsSource.REUTERS : "h1[data-testid = 'Heading']",
    NewsSource.BBC : "div[data-component = 'headline-block']"
}

new_organ_extract_content_tag = {
    NewsSource.YNA : "div.story-news.article",
    NewsSource.YTN : "#CmAdContent.paragraph",
    NewsSource.REUTERS : "div.article-body-module__content__bnXL1",
    NewsSource.BBC : "article"
}

removing_organ_tag = {
    NewsSource.YNA : [
        "table",
        "em",
        "figcaption",
        "p.txt-copyright.adrs",
        "aside",
        "div.related-zone",
        "#newsWriterCarousel01"
    ],

    NewsSource.YTN : [
        "table",
    ],

    NewsSource.REUTERS : [
        "p[data-testid = 'promo-box']"
        "p[data-testid = 'Body']",
        "p[data-testid = 'Tags']",
        "p[data-testid = 'AuthorBio']",
        "p[data-testid = 'ArticleBodyRow']",
    ],

    NewsSource.BBC : [
        "h1",
        "div[data-testid = 'byline']",
        "div[data-component = 'ad-unit']",
        "div[data-component = 'links-block']",
        "div[data-component = 'tags']",
        "aside",
        "footer",
    ]
}

removing_organ_text = {
    NewsSource.YNA : [
    ],

    NewsSource.YTN : [
        "※",
        # "※ '당신의 제보가 뉴스가 됩니다'",
        "[카카오톡]",
        "[전화]",
        "[메일]"
    ],

    NewsSource.REUTERS : [
    ],

    NewsSource.BBC : [
        "Getty Images"
    ]
}