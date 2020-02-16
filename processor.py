from collections import defaultdict
import requests


filepath = 'key_log.txt'

word_count = defaultdict(int)
delimiters = ["Key.space", "$", "&", "^", "&", "*", "+", "=", "~", "{", "}", "[", "]", "Key.enter", "Key.tab"]
common_english_words = [ "the", "be", "to", "of", "and", "a", "in", "that", "have", "I", "it", "for", "not", "on", "with", "he", "as", "you", "do", "at", "this", "but", "his", "by", "from", "they", "we", "say", "her", "she", "or", "an", "will", "my", "one", "all", "would", "there", "their", "what", "so", "up", "out", "if", "about", "who", "get", "which", "go", "me", "when", "make", "can", "like", "time", "no", "just", "him", "know", "take", "people", "into", "year", "your", "good", "some", "could", "them", "see", "other", "than", "then", "now", "look", "only", "come", "its", "over", "think", "also", "back", "after", "use", "two", "how", "our", "work", "first", "well", "way", "even", "new", "want", "because", "any", "these", "give", "day", "most", "us" ]

with open(filepath) as fp:
   line = fp.readline()
   word = ""
   while line:
       line = line.rstrip().replace("'", "")
       if line == "Key.backspace":
           word = word[:-1]
       elif line.isalpha():
           word += line
       elif line in delimiters and word != "" and word not in common_english_words:
           word_count[word.lower()] += 1
           word = ""
       line = fp.readline()

############################################################################################################
       
common_words = defaultdict(list)

for word, _ in sorted(word_count.items(), key = lambda item: -item[1]):
    if len(common_words) == 5:
        break
    
    url = f"https://www.dictionaryapi.com/api/v3/references/thesaurus/json/{word}?key=5ddeb49f-3618-404f-9b92-a01f15b05485"
    response = requests.request("GET", url)
    try:
        synonyms = response.json()[0]['meta']['syns'][0][:5]
        if synonyms:
            common_words[word] = synonyms
    except:
        continue

print(common_words)

############################################################################################################

import smtplib, ssl
from email.mime.text import MIMEText as text

smtp_server = "smtp.gmail.com"
port = 587  # For starttls
sender_email = "dannyattreehacks@gmail.com"
password = "bogaman12"

#receiver_email = input("Enter your email to receive your weekly vocabulary digest!\t")
receiver_email = "datwony@gmail.com"
name = receiver_email.split("@")[0]
message = f"Hi { name },\n\nChecking in with you for your weekly vocabulary digest! This week's top { len(common_words) } replaceable words you used were: \n\n"

for word, synonyms in common_words.items():
    message += f"{ word.title() } could be replaced by { ', '.join(synonyms) }. \n\n"

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
