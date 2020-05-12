# termify
https://devpost.com/software/termify/edit

## Inspiration
Every time I try to learn more vocab words, either in English or a new foreign language, I would have difficulty remembers those words because I would never use them in my day to day life. That's why I created Termify, which basically creates my list of vocab words that I should learn that week! The list of vocab words are created by observing which words I use most often when I am typing on my laptop. By using words that I actually type out often, I would find more use and learn more effectively.

## What it does
Termify is a background process that tracks user keypresses and figures out which words are used most frequently by that user. Termify will then search the thesaurus for the most relevant synonyms to those words and send scheduled email digests to the user with those suggestions. Termify will also search for the translated version of the word in any language the user inputs.

## How I built it
I used Python to create the entire application, which includes the keylogger and the server. I used the pynput library to continuously listen to user keyboard inputs and log those inputs. 

The redundants words will then be passed onto the Webster Merriam Thesaurus API, which would return many synonyms related to the word. (I would then filter this again to return the most related synonyms.) The translated versions of the word are from the Google Translate API.

Up to 5 redundants words are then sent over to the user for a personalized digest on what words they should focus on using the smtplib library on Python. 


## What's next for Termify
I hope to add a voice recording feature in the future by using a mic to track what the user is saying and convert that into text and implement the same features that currently exist. This feature would be optional for users. 
