"""
InsureVoice — Sentiment Analysis Engine
=========================================
Uses TextBlob (built on NLTK) for polarity/subjectivity scoring.
Also applies an insurance-domain keyword boost for better accuracy.

SETUP (run once):
    python -m nltk.downloader punkt averaged_perceptron_tagger
"""

import re
import nltk
from textblob import TextBlob

# ── Download required NLTK data (runs once) ──
def ensure_nltk_data():
    """Download NLTK datasets if not already present."""
    datasets = [
        'punkt', 'averaged_perceptron_tagger',
        'brown', 'stopwords', 'wordnet'
    ]
    for ds in datasets:
        try:
            nltk.data.find(f'tokenizers/{ds}')
        except LookupError:
            try:
                nltk.download(ds, quiet=True)
            except Exception:
                pass  # Non-critical; TextBlob still works without all

ensure_nltk_data()


# ═══════════════════════════════════════════
#  DOMAIN-SPECIFIC KEYWORD DICTIONARIES
#  (Insurance context boosts accuracy beyond TextBlob defaults)
# ═══════════════════════════════════════════

# Strong negative insurance terms
INSURANCE_NEGATIVE = {
    "rejected", "reject", "rejection", "deny", "denied", "denial",
    "delayed", "delay", "slow", "never", "fraud", "scam", "cheat",
    "cheated", "lied", "false", "mislead", "misleading", "hidden",
    "hidden charges", "overcharged", "overcharge", "poor", "terrible",
    "horrible", "useless", "pathetic", "worst", "disgusting", "awful",
    "nightmare", "frustrated", "frustrating", "harassment", "harass",
    "ignored", "ignore", "rude", "arrogant", "incompetent", "unprofessional",
    "no response", "unresponsive", "closed", "lapse", "expired", "cancelled",
    "misrepresentation", "exclusion", "pre-existing", "preexisting",
    "bad faith", "breach", "lawsuit", "negligent", "negligence",
    "not processed", "not paid", "not covered", "not reimbursed",
    "claim denied", "claim rejected", "settlement refused",
}

# Strong positive insurance terms
INSURANCE_POSITIVE = {
    "approved", "approve", "approval", "paid", "reimbursed", "reimbursement",
    "fast", "quick", "smooth", "easy", "excellent", "great", "amazing",
    "wonderful", "outstanding", "best", "perfect", "good", "happy",
    "satisfied", "transparent", "honest", "helpful", "professional",
    "responsive", "efficient", "hassle-free", "hassle free", "prompt",
    "quick settlement", "claim settled", "claim approved", "covered",
    "trust", "trustworthy", "reliable", "recommend", "recommended",
    "impressive", "superb", "thank you", "grateful", "pleased",
    "seamless", "speedy", "timely", "fair", "reasonable", "affordable",
}

# Intensifiers and negation words
INTENSIFIERS  = {"very", "extremely", "absolutely", "totally", "completely", "highly", "so", "really"}
NEGATORS      = {"not", "never", "no", "don't", "didn't", "doesn't", "isn't", "wasn't", "aren't", "weren't", "can't"}


def preprocess_text(text: str) -> str:
    """
    Clean and normalize input text for analysis.
    - Lowercase
    - Remove HTML tags
    - Normalize whitespace
    - Keep punctuation (needed for TextBlob sentence-level analysis)
    """
    text = text.strip()
    text = re.sub(r'<[^>]+>', ' ', text)               # strip HTML
    text = re.sub(r'http\S+|www\S+', '', text)         # remove URLs
    text = re.sub(r'\s+', ' ', text)                   # normalize spaces
    return text


def extract_keywords(text: str) -> dict:
    """
    Find positive and negative insurance keywords present in the text.
    Returns a dict with 'positive' and 'negative' keyword lists.
    """
    lower = text.lower()
    pos_found = [w for w in INSURANCE_POSITIVE if w in lower]
    neg_found = [w for w in INSURANCE_NEGATIVE if w in lower]
    return {"positive": sorted(pos_found), "negative": sorted(neg_found)}


def domain_score(text: str) -> float:
    """
    Calculate a domain-specific score based on insurance keyword matching.
    Returns a float between roughly -1.0 and +1.0.
    Each keyword hit adds ±0.15; intensifiers add 0.05 bonus.
    Negation words flip keyword scores.
    """
    words  = text.lower().split()
    score  = 0.0
    window = 3  # words to look back for negation

    for i, word in enumerate(words):
        # Check negation in preceding window
        context  = words[max(0, i-window):i]
        negated  = any(neg in context for neg in NEGATORS)
        intensity = 1.2 if any(intens in context for intens in INTENSIFIERS) else 1.0

        if word in INSURANCE_POSITIVE:
            delta = 0.15 * intensity
            score += (-delta if negated else delta)
        elif word in INSURANCE_NEGATIVE:
            delta = 0.15 * intensity
            score += (delta if negated else -delta)

    # Normalize to [-1, +1]
    return max(-1.0, min(1.0, score))


def sentiment_label(polarity: float) -> tuple:
    """
    Convert combined polarity score to a human-readable label.

    Returns:
        (sentiment_str, emoji_label, confidence)
    """
    if polarity > 0.10:
        sentiment   = "positive"
        label       = "Positive 😊"
        confidence  = "high" if polarity > 0.40 else "medium"
    elif polarity < -0.10:
        sentiment   = "negative"
        label       = "Negative 😞"
        confidence  = "high" if polarity < -0.40 else "medium"
    else:
        sentiment   = "neutral"
        label       = "Neutral 😐"
        confidence  = "medium"
    return sentiment, label, confidence


def analyze_sentiment(text: str) -> dict:
    """
    Main function: analyze the sentiment of an insurance review.

    Args:
        text (str): Raw review text.

    Returns:
        dict with keys:
          - sentiment      : 'positive' | 'negative' | 'neutral'
          - polarity       : float  [-1, 1]  (combined TextBlob + domain)
          - subjectivity   : float  [0, 1]   (TextBlob)
          - label          : human-readable sentiment string
          - confidence     : 'high' | 'medium'
          - textblob_score : raw TextBlob polarity
          - domain_score   : domain keyword score
          - keywords       : {'positive': [...], 'negative': [...]}
          - word_count     : int
          - text_preview   : first 100 chars
    """
    # 1. Clean text
    cleaned = preprocess_text(text)

    # 2. TextBlob analysis
    blob             = TextBlob(cleaned)
    tb_polarity      = blob.sentiment.polarity      # [-1, 1]
    tb_subjectivity  = blob.sentiment.subjectivity  # [0, 1]

    # 3. Domain keyword score
    dom_score = domain_score(cleaned)

    # 4. Weighted combination: 40% TextBlob, 60% domain keywords
    #    (Insurance domain keywords are more reliable than generic lexicon)
    combined = (tb_polarity * 0.4) + (dom_score * 0.6)

    # 5. Convert to label
    sentiment, label, confidence = sentiment_label(combined)

    # 6. Extract keywords
    keywords = extract_keywords(cleaned)

    return {
        "sentiment":       sentiment,
        "polarity":        round(combined, 4),
        "subjectivity":    round(tb_subjectivity, 4),
        "label":           label,
        "confidence":      confidence,
        "textblob_score":  round(tb_polarity, 4),
        "domain_score":    round(dom_score, 4),
        "keywords":        keywords,
        "word_count":      len(cleaned.split()),
        "text_preview":    cleaned[:100] + ("…" if len(cleaned) > 100 else ""),
    }


def batch_analyze(texts: list) -> list:
    """
    Analyze a list of review texts.

    Args:
        texts (list): List of raw review strings.

    Returns:
        list of sentiment result dicts (same schema as analyze_sentiment).
    """
    results = []
    for text in texts:
        if not isinstance(text, str) or not text.strip():
            results.append({"error": "Invalid or empty text."})
        else:
            results.append(analyze_sentiment(text))
    return results


# ═══════════════════════════════════════════
#  QUICK CLI TEST (run: python sentiment.py)
# ═══════════════════════════════════════════
if __name__ == "__main__":
    test_cases = [
        "The claim was processed quickly and I received the full amount within 3 days. Excellent service!",
        "My claim was rejected without any valid reason. Complete fraud. Never trust this company.",
        "The service was average. Claim took some time but was eventually approved.",
        "Worst insurance company I have ever dealt with. Hidden charges everywhere and claim denied.",
        "Very smooth experience. Transparent process, good customer support and fast settlement.",
        "The claim is pending for 6 months now. No response from the customer service team.",
    ]

    print("\n" + "="*70)
    print("  InsureVoice Sentiment Analysis — Test Cases")
    print("="*70)
    for i, t in enumerate(test_cases, 1):
        result = analyze_sentiment(t)
        print(f"\n[{i}] TEXT    : {t[:70]}…")
        print(f"    RESULT  : {result['label']}  (polarity={result['polarity']:+.3f}, confidence={result['confidence']})")
        if result['keywords']['positive']:
            print(f"    POS KW  : {', '.join(result['keywords']['positive'][:5])}")
        if result['keywords']['negative']:
            print(f"    NEG KW  : {', '.join(result['keywords']['negative'][:5])}")
    print("\n" + "="*70 + "\n")
