import json
from etnltk import Amharic
from etnltk.common.preprocessing import remove_emojis, remove_digits, remove_english_chars
from etnltk.common.ethiopic import remove_ethiopic_punctuation
import re

def clean_text(text):
    # Preprocess Amharic text
    return Amharic(text).cleaned


def tokenize_text(text):
    # Use etnltk's tokenizer for Amharic
    doc = Amharic(text)
    return [str(w) for w in doc.words]

def label_tokens(tokens):
    print("\n Label each token (default = O). Options: B-Product, I-Product, B-PRICE, I-PRICE, B-LOC, I-LOC, O")
    labeled = []
    for token in tokens:
        label = input(f"{token}: ").strip() or "O"
        labeled.append((token, label))
    return labeled

def write_conll(labeled_sentences, filepath="labeled_data.conll"):
    with open(filepath, "a", encoding="utf-8") as f:
        for tokens in labeled_sentences:
            for tok, lbl in tokens:
                f.write(f"{tok}\t{lbl}\n")
            f.write("\n")

def load_messages(json_path):
    with open(json_path, encoding="utf-8") as f:
        data = json.load(f)
    return [msg["message"] for msg in data]

def main():
    json_path = input("Enter path to Telegram JSON file: ").strip()
    messages = load_messages(json_path)
    labeled_all = []

    for i, msg in enumerate(messages[:50], 1):
        print(f"\n--- Message #{i} ---\n{msg}\n")
        clean = clean_text(msg)
        tokens = tokenize_text(clean)
        labeled = label_tokens(tokens)
        labeled_all.append(labeled)

    write_conll(labeled_all)
    print("\n Saved labeled data to 'labeled_data.conll'")

if __name__ == "__main__":
    main()
