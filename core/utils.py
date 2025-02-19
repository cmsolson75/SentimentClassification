import re
import spacy


def rm_link(text):
    return re.sub(r"https?://\S+|www\.\S+", "", text)


def rm_punctuation(text):
    return re.sub(
        r"[\"\#\$\%\&\'\(\)\*\+\/\:\;\<\=\>\@\[\\\]\^\_\`\{\|\}\~]", " ", text
    )


def rm_html(text):
    return re.sub(r"<[^>]+>", "", text)


def space_bt_punctuation(text):
    pattern = r"([.,!?-])"
    s = re.sub(pattern, r" \1", text)
    s = re.sub(r"\s{2,}", " ", s)
    return s


def rm_number(text):
    return re.sub(r"\d+", "", text)


def rm_whitespaces(text):
    return re.sub(r" +", " ", text)


def rm_nonascii(text):
    return re.sub(r"[^\x00-\x7f]", r"", text)


def clean_pipeline(text):
    text = text.lower()
    text = rm_link(text)
    text = rm_punctuation(text)
    text = rm_html(text)
    text = rm_number(text)
    text = rm_whitespaces(text)
    text = rm_nonascii(text)
    return text


# Need to make this a special class for handling this shit,
nlp = spacy.load("en_core_web_sm")


def preprocess_pipeline(text):
    text = clean_pipeline(text)
    doc = nlp(text)
    return " ".join([token.lemma_ for token in doc])