import html
import math
import re


def get_reading_time(text: str):
    regexp = re.compile('<.*?>')
    cleaned_text = re.sub(regexp, '', text)
    cleaned_text = cleaned_text.strip()
    words_count = cleaned_text.count(' ') + 1
    return math.ceil(words_count / 250)


def get_preview(text: str):
    regexp = re.compile('<.*?>')
    cleaned_text = html.unescape(re.sub(regexp, '', text))[:250]
    current_length = 0
    preview = ''
    words = cleaned_text.split()
    for word in words:
        current_length += len(word)
        preview += word + ' '
    preview = preview.strip()
    # if the words are too long (longer than 90 chars that can fit into preview width, insert spaces)
    last_pos = 0
    while len(preview) - last_pos > 90:
        space_pos = preview.find(' ', last_pos)
        if space_pos - last_pos > 90 or space_pos == -1:
            last_pos += 90
            head = preview[:last_pos]
            tail = preview[last_pos:]
            preview = head + ' ' + tail
            last_pos += 1
        else:
            last_pos = space_pos + 1
    return preview + '...'
