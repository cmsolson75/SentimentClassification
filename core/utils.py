import re
import spacy

# Precompile for production
LINK_PATTERN = re.compile(r"https?://\S+|www\.\S+")
PUNCTUATION_PATTERN = re.compile(
    r"[\"\#\$\%\&\'\(\)\*\+\/\:\;\<\=\>\@\[\\\]\^\_\`\{\|\}\~]"
)
HTML_PATTERN = re.compile(r"<[^>]+>")
NUMBER_PATTERN = re.compile(r"\d+")
NONASCII_PATTERN = re.compile(r"[^\x00-\x7f]")
NORMALIZE_WHITESPACE_PATTERN = re.compile(r" +")


def rm_link(text: str) -> str:
    """Remove URLs from the text."""
    return LINK_PATTERN.sub("", text)


def rm_punctuation(text: str) -> str:
    """Remove most punctuation, keeping standard sentence punctuation."""
    return PUNCTUATION_PATTERN.sub(" ", text)


def rm_html(text: str) -> str:
    """Remove HTML tags."""
    return HTML_PATTERN.sub("", text)


def rm_number(text: str) -> str:
    """Remove numeric characters."""
    return NUMBER_PATTERN.sub("", text)


def normalize_whitespaces(text: str) -> str:
    """Trim excessive spaces and normalize spacing."""
    return NORMALIZE_WHITESPACE_PATTERN.sub(" ", text)


def rm_nonascii(text: str) -> str:
    """Remove non-ASCII characters."""
    return NONASCII_PATTERN.sub("", text)


def normalize_text(text: str) -> str:
    """Normalize incoming text to a pre-defined standard"""
    text = text.lower()
    text = rm_link(text)
    text = rm_punctuation(text)
    text = rm_html(text)
    text = rm_number(text)
    text = rm_nonascii(text)
    return normalize_whitespaces(text)


def preprocess_text(text: str, nlp: spacy.language.Language) -> str:
    """
    Normalize text, then apply tokenization and lemmatization using spaCy.

    Args:
        text (str): Input to be processed
        nlp (spacy.language.Language): Preloaded spaCy language model.

    Returns:
        str: Processed text with tokens lemmatized.
    """
    text = normalize_text(text)
    doc = nlp(text)
    return " ".join(token.lemma_ for token in doc)
