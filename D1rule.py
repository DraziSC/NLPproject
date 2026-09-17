import nltk

nltk.download('popular')

# do a quick check to see if the user has the necessary NLTK data files
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')

    """
A class for simple chatbots.  These perform simple pattern matching on sentences
typed by users, and respond with automatically generated sentences.

These chatbots may not work using the windows command line or the
windows IDLE GUI.
"""

from nltk.chat.eliza import eliza_chat
from nltk.chat.iesha import iesha_chat
from nltk.chat.rude import rude_chat
from nltk.chat.suntsu import suntsu_chat
from nltk.chat.util import Chat
from nltk.chat.zen import zen_chat

bots = [
    (eliza_chat, "Eliza (psycho-babble)"),
    (iesha_chat, "Iesha (teen anime junky)"),
    (rude_chat, "Rude (abusive bot)"),
    (suntsu_chat, "Suntsu (Chinese sayings)"),
    (zen_chat, "Zen (gems of wisdom)"),
]


def chatbots():
    print("Which chatbot would you like to talk to?")
    botcount = len(bots)
    for i in range(botcount):
        print("  %d: %s" % (i + 1, bots[i][1]))
    while True:
        choice = input(f"\nEnter a number in the range 1-{botcount}: ").strip()
        if choice.isdigit() and (int(choice) - 1) in range(botcount):
            break
        else:
            print("   Error: bad chatbot number")

    chatbot = bots[int(choice) - 1][0]
    chatbot()

chatbots()
