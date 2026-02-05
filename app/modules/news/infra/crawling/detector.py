from langdetect import detect
from langdetect.lang_detect_exception import LangDetectException

from app.common.config.logging import logger

def detect_language(content: str) -> str | None:
    try:
        lang = detect(content)
        return lang
    except(LangDetectException, ValueError) as e:
        # logger.error(type(e), e)
        return None
