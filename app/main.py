from fastapi import FastAPI, Request, Depends, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from .database import Base, engine, get_db
from .models import SupportMessage
from .ai_service import analyze_message

Base.metadata.create_all(bind=engine)

app = FastAPI(title="AI Support Inbox")

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

ui_text = {
    "en": {
        "title": "AI Support Inbox",
        "subtitle": "Customer message analysis dashboard",
        "customer_name": "Customer Name",
        "customer_name_placeholder": "Enter customer name",
        "customer_message": "Customer Message",
        "customer_message_placeholder": "Enter customer message",
        "language": "Response Language",
        "analyze_button": "Analyze Message",
        "analyzed_messages": "Analyzed Messages",
        "no_messages": "No analyzed messages yet.",
        "message": "Message",
        "category": "Category",
        "sentiment": "Sentiment",
        "priority": "Priority",
        "suggested_reply": "Suggested Reply",
        "created_at": "Created At",
        "delete": "Delete",
        "delete_all": "Delete All",
        "clear_filters": "Clear Filters",
        "records": "records",
        "all_categories": "All Categories",
        "all_priorities": "All Priorities",
        "filters": "Filters",
        "success_message": "Message analyzed successfully.",
    },
    "tr": {
        "title": "AI Destek Gelen Kutusu",
        "subtitle": "Müşteri mesajı analiz paneli",
        "customer_name": "Müşteri Adı",
        "customer_name_placeholder": "Müşteri adını girin",
        "customer_message": "Müşteri Mesajı",
        "customer_message_placeholder": "Müşteri mesajını girin",
        "language": "Yanıt Dili",
        "analyze_button": "Mesajı Analiz Et",
        "analyzed_messages": "Analiz Edilen Mesajlar",
        "no_messages": "Henüz analiz edilmiş mesaj yok.",
        "message": "Mesaj",
        "category": "Kategori",
        "sentiment": "Duygu Durumu",
        "priority": "Öncelik",
        "suggested_reply": "Önerilen Yanıt",
        "created_at": "Oluşturulma",
        "delete": "Sil",
        "delete_all": "Tümünü Sil",
        "clear_filters": "Filtreleri Temizle",
        "records": "kayıt",
        "all_categories": "Tüm Kategoriler",
        "all_priorities": "Tüm Öncelikler",
        "filters": "Filtreler",
        "success_message": "Mesaj başarıyla analiz edildi.",
    },
}


def get_priority_class(priority: str) -> str:
    value = priority.lower()
    if value in ["high", "yüksek"]:
        return "priority-high"
    if value in ["medium", "orta"]:
        return "priority-medium"
    return "priority-low"


def get_sentiment_class(sentiment: str) -> str:
    value = sentiment.lower()
    if value in ["negative", "olumsuz"]:
        return "sentiment-negative"
    if value in ["neutral", "nötr"]:
        return "sentiment-neutral"
    return "sentiment-positive"


@app.get("/", response_class=HTMLResponse)
def home(
    request: Request,
    db: Session = Depends(get_db),
    lang: str = "en",
    category_filter: str = "",
    priority_filter: str = "",
    success: str = ""
):
    messages = db.query(SupportMessage).order_by(SupportMessage.id.desc()).all()
    selected_ui = ui_text.get(lang, ui_text["en"])

    all_categories = sorted(list(set(msg.category for msg in messages)))
    all_priorities = sorted(list(set(msg.priority for msg in messages)))

    enriched_messages = []
    for item in messages:
        enriched_item = {
            "id": item.id,
            "customer_name": item.customer_name,
            "message": item.message,
            "category": item.category,
            "sentiment": item.sentiment,
            "priority": item.priority,
            "suggested_reply": item.suggested_reply,
            "created_at": item.created_at.strftime("%d.%m.%Y %H:%M") if item.created_at else "-",
            "priority_class": get_priority_class(item.priority),
            "sentiment_class": get_sentiment_class(item.sentiment),
        }
        enriched_messages.append(enriched_item)

    if category_filter:
        enriched_messages = [
            item for item in enriched_messages
            if item["category"] == category_filter
        ]

    if priority_filter:
        enriched_messages = [
            item for item in enriched_messages
            if item["priority"] == priority_filter
        ]

    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "messages": enriched_messages,
            "ui": selected_ui,
            "lang": lang,
            "category_filter": category_filter,
            "priority_filter": priority_filter,
            "all_categories": all_categories,
            "all_priorities": all_priorities,
            "success": success,
        }
    )


@app.post("/analyze")
def analyze(
    customer_name: str = Form(...),
    message: str = Form(...),
    language: str = Form(...),
    db: Session = Depends(get_db)
):
    result = analyze_message(message, language)

    new_message = SupportMessage(
        customer_name=customer_name,
        message=message,
        category=result["category"],
        sentiment=result["sentiment"],
        priority=result["priority"],
        suggested_reply=result["suggested_reply"],
    )

    db.add(new_message)
    db.commit()

    return RedirectResponse(url=f"/?lang={language}&success=1", status_code=303)


@app.post("/delete/{message_id}")
def delete_message(message_id: int, lang: str = "en", db: Session = Depends(get_db)):
    message = db.query(SupportMessage).filter(SupportMessage.id == message_id).first()
    if message:
        db.delete(message)
        db.commit()

    return RedirectResponse(url=f"/?lang={lang}", status_code=303)


@app.post("/delete-all")
def delete_all_messages(lang: str = "en", db: Session = Depends(get_db)):
    db.query(SupportMessage).delete()
    db.commit()
    return RedirectResponse(url=f"/?lang={lang}", status_code=303)