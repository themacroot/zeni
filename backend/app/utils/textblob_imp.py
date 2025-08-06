from textblob import TextBlob

def spell_correct_textblob(text: str) -> str:
    blob = TextBlob(text)
    return str(blob.correct())
