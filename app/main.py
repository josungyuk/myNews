from fastapi import FastAPI
from fastapi import Request
from fastapi.responses import JSONResponse
from google.genai import errors as genai_errors
from app.news.controller.news_controller import router as news_router
from app.summary.controller.summary_controller import router as summary_router
from app.rag.controller.rag_controller import router as rag_router

app = FastAPI(title="News Service")


@app.exception_handler(genai_errors.APIError)
async def handle_gemini_api_error(
    request: Request,
    exc: genai_errors.APIError,
) -> JSONResponse:
    if exc.code == 429:
        message = "Gemini API quota was exceeded. Please try again later."
        status_code = 429
    elif exc.code == 503:
        message = "Gemini is temporarily unavailable. Please try again later."
        status_code = 503
    else:
        message = "Gemini API request failed."
        status_code = 502

    return JSONResponse(
        status_code=status_code,
        content={"detail": message},
        headers={"Retry-After": "30"} if status_code in {429, 503} else None,
    )

app.include_router(news_router)
app.include_router(summary_router)
app.include_router(rag_router)
