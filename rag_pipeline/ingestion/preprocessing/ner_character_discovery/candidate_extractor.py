import spacy
from collections import Counter

nlp = spacy.load("en_core_web_sm")

def extract_person_candidates(text: str, min_freq: int = 3):
    """
    Returns Counter of PERSON names found in text.
    """
    print("extract_person_candidates called ")
    doc = nlp(text)
    persons = []

    for ent in doc.ents:
        if ent.label_ == "PERSON":
            name = ent.text.strip()
            if len(name.split()) <= 4:  # avoid long junk
                persons.append(name)

    freq = Counter(persons)
    print(Counter({
        name: count
        for name, count in freq.items()
        if count >= min_freq
    }))
    # filter rare noise
    return Counter({
        name: count
        for name, count in freq.items()
        if count >= min_freq
    })
