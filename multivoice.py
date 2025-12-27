from gtts import gTTS
from io import BytesIO
import pygame
from langdetect import detect, DetectorFactory
import re
import math
import time
DetectorFactory.seed = 0
pygame.mixer.init()
WPM = 130
LANGUAGE_MAP = {
    'mk': 'ru',
    'no': 'nb',
    'iw': 'he',
    'tl': 'fil',
}
def detect_language(text):
    try:
        lang = detect(text)
        return LANGUAGE_MAP.get(lang, lang)
    except:
        return 'en'
def speak_gtts(text, lang_code):
    try:
        tts_stream = BytesIO()
        tts = gTTS(text=text, lang=lang_code)
        tts.write_to_fp(tts_stream)
        tts_stream.seek(0)
        pygame.mixer.music.load(tts_stream, 'mp3')
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)
    except Exception as e:
        print(f"gTTS error: {e}")
def split_sentences(text):
    sentences = re.split(r'(?<=[.!?])\s+', text)
    return [s.strip() for s in sentences if s.strip()]
def calculate_dynamic_delay(sentence, total_words):
    words = len(sentence.split())
    base_duration = (words / WPM) * 60
    proportion = words / total_words if total_words else 1
    return max(1.0, base_duration * proportion)
def main():
    print("=== Ultimate Audiobook TTS ===")
    print("Type 'exit' to quit.")
    print("Enter text in any single language (auto-detected).")
    print("-------------------------------------------")
    while True:
        text = input("Enter your text: ").strip()
        if text.lower() == 'exit':
            print("Program terminated.")
            break
        if not text:
            continue
        lang = detect_language(text)
        print(f"Detected language: {lang}")
        sentences = split_sentences(text)
        total_words = sum(len(s.split()) for s in sentences)
        for sentence in sentences:
            print(f"Speaking: {sentence}")
            speak_gtts(sentence, lang)
            delay = calculate_dynamic_delay(sentence, total_words)
            time.sleep(delay * 0.05)
        time.sleep(0.2)
if __name__ == "__main__":
    main()
# マイ トゥムヘ チョドナ チャフタ フー