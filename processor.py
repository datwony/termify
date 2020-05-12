from collections import defaultdict
import requests
from googletrans import Translator

filepath = 'key_log.txt'

word_count = defaultdict(int)
delimiters = ["Key.space", "$", "&", "^", "&", "*", "+", "=", "~", "{", "}", "[", "]", "Key.enter", "Key.tab"]
common_english_words = [ "is", "Is", "the", "be", "to", "of", "and", "a", "in", "that", "have", "I", "it", "for", "not", "on", "with", "he", "as", "you", "do", "at", "this", "but", "his", "by", "from", "they", "we", "say", "her", "she", "or", "an", "will", "my", "one", "all", "would", "there", "their", "what", "so", "up", "out", "if", "about", "who", "get", "which", "go", "me", "when", "make", "can", "like", "time", "no", "just", "him", "know", "take", "people", "into", "year", "your", "good", "some", "could", "them", "see", "other", "than", "then", "now", "look", "only", "come", "its", "over", "think", "also", "back", "after", "use", "two", "how", "our", "work", "first", "well", "way", "even", "new", "want", "because", "any", "these", "give", "day", "most", "us" ]

with open(filepath) as fp:
   line = fp.readline()
   word = ""
   while line:
       line = line.rstrip().replace("'", "")
       if line == "Key.backspace":
           word = word[:-1]
       elif line.isalpha():
           word += line
       elif line in delimiters:
           if len(word) > 1 and word not in common_english_words:
               word_count[word.lower()] += 1
           word = ""
       
       line = fp.readline()

############################################################################################################
trans = Translator()     
common_words = defaultdict(dict)

for word, _ in sorted(word_count.items(), key = lambda item: -item[1]):
    if len(common_words) == 5:
        break
    
    key = None # GET API KEY FROM DICTIONARYAPI.COM
    url = f"https://www.dictionaryapi.com/api/v3/references/thesaurus/json/{word}?key={key}"
    response = requests.request("GET", url)
    try:
        synonyms = response.json()[0]['meta']['syns'][0][:5]
        translated = trans.translate(word, dest = 'ko')
        if synonyms:
            common_words[word]['syn'] = synonyms
            common_words[word]['trans'] = (translated.text, translated.pronunciation)
    except:
        continue

print(common_words)

############################################################################################################

import smtplib, ssl
from email.mime.text import MIMEText as text

smtp_server = "smtp.gmail.com"
port = 587  # For starttls
sender_email = "example.gmail.com"
password = "example"

receiver_email = input("Enter your email to receive your weekly vocabulary digest!\t")

name = receiver_email.split("@")[0]
message = f"Hi { name }!\n\nJust checking in with you for your weekly vocabulary digest! This week's top { len(common_words) } replaceable words you used were: \n\n"

for word, d in common_words.items():
    message += f"{ word.title() }\nTry using one of these words: { ', '.join(d['syn']) }.\nIn Korean {word} is {d['trans'][0]}"
    if d['trans'][1]:
        message += f", which is pronunciated {d['trans'][1]}.\n\n"
    else:
        message += ".\n\n"

message += f" See you next time!\n\t - Danny from Termify"

m = text(message)
m['Subject'] = "Termify Weekly Digest"
m['From'] = "Danny from Termify"
m['To'] = receiver_email

context = ssl.create_default_context()
with smtplib.SMTP(smtp_server, port) as server:
    server.ehlo()  # Can be omitted
    server.starttls(context=context)
    server.ehlo()  # Can be omitted
    server.login(sender_email, password)
    server.sendmail(sender_email, receiver_email, m.as_string())
    server.quit()

f = open('key_log.txt', 'w')
f.close()
