from enum import Enum

class NewsSource(Enum):
    YNA = "yna"
    YTN = "ytn"
    REUTERS = "reuters"
    BBC = "bbc"
    GUARDIAN = "guardian"
    NPR = "npr"

class NewsType(Enum):
    ECONOMY = "economy"
    SOCIETY = "society"
    WORLD = "world"

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
    NewsSource.BBC : "https://www.bbc.com",
    NewsSource.GUARDIAN : "https://www.theguardian.com",
    NewsSource.NPR : "https://www.npr.org",
}

news_organ_type = {
    NewsSource.YNA : {
        NewsType.ECONOMY : "economy/all",
        NewsType.WORLD : "international/all"
    },

    NewsSource.YTN : {
        NewsType.ECONOMY : "news/list.php?mcd=0102",
        NewsType.WORLD : "news/list.php?mcd=0104"
    },

    NewsSource.REUTERS : {
        NewsType.WORLD : {
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
        NewsType.WORLD : "news/us-canada"
    },

    NewsSource.GUARDIAN : {
        NewsType.ECONOMY : "business/economics",
        NewsType.WORLD : "international"
    },

    NewsSource.NPR : {
        NewsType.ECONOMY : "sections/economy",
        NewsType.WORLD : "sections/world"
    }
}

news_language = {
    NewsSource.YNA : "kr",
    NewsSource.YTN : "kr",
    NewsSource.REUTERS : "en",
    NewsSource.BBC : "en",
    NewsSource.GUARDIAN : "en",
    NewsSource.NPR : "en",
}

news_organ_content_tag = {  
    NewsSource.YNA : ".list01 .item-box01 .img-con01 a[href ^= 'https://www.yna.co.kr/view/']",
    NewsSource.YTN : ".title a[href ^= 'https://www.ytn.co.kr/_ln/']",
    NewsSource.REUTERS : ".TitleLink a[href ^= '/worlds/']",
    NewsSource.BBC : "a[href ^= '/news/articles/'][data-testid=internal-link]:has(p)",
    NewsSource.GUARDIAN : "a[href ^= '/'][data-link-name ^= 'news'], .sublinks a[href ^= '/']:not([href *= '/live'])",
    NewsSource.NPR : "section#main-section h2.title a[href ^= 'https']"
}

news_organ_extract_title_tag = {
    NewsSource.YNA : "h1.tit01",
    NewsSource.YTN : "h2.news_title",
    NewsSource.REUTERS : "h1[data-testid = 'Heading']",
    NewsSource.BBC : "div[data-component = 'headline-block']",
    NewsSource.GUARDIAN : "h1",
    NewsSource.NPR : "h1"
}

news_organ_extract_date_tag = {
    NewsSource.YNA : "#newsUpdateTime01",
    NewsSource.YTN : "div.date",
    NewsSource.BBC : "time",
    NewsSource.GUARDIAN : "[data-gu-name = 'dateline']",
    NewsSource.NPR : "time"
}

news_organ_date_tag_value = {
    NewsSource.YNA : "data-published-time",
    NewsSource.YTN : None,
    NewsSource.BBC : "datetime",
    NewsSource.GUARDIAN : None,
    NewsSource.NPR : "datetime",
}

news_organ_extract_content_tag = {
    NewsSource.YNA : "div.story-news.article",
    NewsSource.YTN : "div.paragraph#CmAdContent",
    NewsSource.REUTERS : "div.article-body-module__content__bnXL1",
    NewsSource.BBC : "article",
    NewsSource.GUARDIAN : "div#maincontent",
    NewsSource.NPR : "div#storytext"
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
        "p[data-testid = 'promo-box']",
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
    ],

    NewsSource.GUARDIAN : [

    ],

    NewsSource.NPR : [

    ],
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
    ],

    NewsSource.GUARDIAN : [

    ],

    NewsSource.NPR : [

    ],
}