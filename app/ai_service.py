def analyze_message(message: str, language: str = "en") -> dict:
    text = message.lower()

    category_key = "general"
    sentiment_key = "neutral"
    priority_key = "medium"

    if any(word in text for word in ["refund", "return", "cancel", "iade", "iptal"]):
        category_key = "refund_return"

    elif any(word in text for word in ["late", "delay", "shipping", "cargo", "delivery", "geç", "kargo", "teslimat"]):
        category_key = "shipping_issue"

    elif any(word in text for word in ["broken", "damaged", "defective", "problem", "bozuk", "hasarlı", "sorun"]):
        category_key = "product_issue"

    elif any(word in text for word in ["price", "cost", "discount", "fiyat", "indirim", "ücret"]):
        category_key = "pricing"

    if any(word in text for word in [
        "angry", "bad", "terrible", "worst", "unacceptable",
        "kötü", "rezalet", "kabul edilemez", "sinirliyim", "berbat"
    ]):
        sentiment_key = "negative"
        priority_key = "high"

    elif any(word in text for word in [
        "love", "great", "perfect", "thanks",
        "harika", "mükemmel", "teşekkürler", "teşekkür ederim",
        "mutlu", "memnun", "çok iyi", "yardımcı oldunuz", "çok yardımcı oldunuz"
    ]):
        sentiment_key = "positive"
        priority_key = "low"

    translations = {
        "en": {
            "categories": {
                "general": "General Inquiry",
                "refund_return": "Refund / Return",
                "shipping_issue": "Shipping Issue",
                "product_issue": "Product Issue",
                "pricing": "Pricing",
            },
            "sentiments": {
                "positive": "Positive",
                "neutral": "Neutral",
                "negative": "Negative",
            },
            "priorities": {
                "low": "Low",
                "medium": "Medium",
                "high": "High",
            },
            "replies": {
                "general": "Thank you for contacting us. Our team will review your request shortly.",
                "refund_return": (
                    "We are sorry for the inconvenience. Please share your order number so we can "
                    "review your refund or return request as quickly as possible."
                ),
                "shipping_issue": (
                    "We understand your concern about the delivery. Please share your order number "
                    "and we will check the shipping status for you."
                ),
                "product_issue": (
                    "We are sorry to hear that you had an issue with the product. Please send us "
                    "your order number and a short description of the problem."
                ),
                "pricing": (
                    "Thank you for your message. We would be happy to provide more information about "
                    "pricing, campaigns, or current discounts."
                ),
            },
        },
        "tr": {
            "categories": {
                "general": "Genel Talep",
                "refund_return": "İade / Geri Ödeme",
                "shipping_issue": "Kargo Sorunu",
                "product_issue": "Ürün Sorunu",
                "pricing": "Fiyatlandırma",
            },
            "sentiments": {
                "positive": "Olumlu",
                "neutral": "Nötr",
                "negative": "Olumsuz",
            },
            "priorities": {
                "low": "Düşük",
                "medium": "Orta",
                "high": "Yüksek",
            },
            "replies": {
                "general": "Bizimle iletişime geçtiğiniz için teşekkür ederiz. Ekibimiz talebinizi kısa süre içinde inceleyecektir.",
                "refund_return": (
                    "Yaşadığınız olumsuzluk için üzgünüz. İade veya geri ödeme talebinizi hızlıca inceleyebilmemiz için "
                    "lütfen sipariş numaranızı bizimle paylaşın."
                ),
                "shipping_issue": (
                    "Teslimat konusundaki endişenizi anlıyoruz. Lütfen sipariş numaranızı paylaşın, "
                    "kargo durumunu sizin için kontrol edelim."
                ),
                "product_issue": (
                    "Ürünle ilgili sorun yaşadığınızı duyduğumuza üzüldük. Lütfen sipariş numaranızı ve "
                    "sorunun kısa bir açıklamasını bizimle paylaşın."
                ),
                "pricing": (
                    "Mesajınız için teşekkür ederiz. Fiyatlandırma, kampanyalar veya mevcut indirimler hakkında "
                    "size memnuniyetle bilgi verebiliriz."
                ),
            },
        },
    }

    selected_lang = translations.get(language, translations["en"])

    return {
        "category": selected_lang["categories"][category_key],
        "sentiment": selected_lang["sentiments"][sentiment_key],
        "priority": selected_lang["priorities"][priority_key],
        "suggested_reply": selected_lang["replies"][category_key],
    }