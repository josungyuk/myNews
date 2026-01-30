from langdetect import detect
from langdetect.lang_detect_exception import LangDetectException

def detect_language(content: str) -> str | None:
    try:
        lang = detect(content)
        return lang
    except(LangDetectException, ValueError):
        return None
