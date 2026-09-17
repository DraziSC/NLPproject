import nltk

#nltk.download('popular')

# do a quick check to see if the user has the necessary NLTK data files
#try:
#    nltk.data.find('tokenizers/punkt')
#except LookupError:
#    nltk.download('punkt')

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
from nltk.chat.util import Chat, reflections
from nltk.chat.zen import zen_chat

from nltk.chat.util import Chat, reflections

persona_pairs = [
    [
        r"hello|hi|hey",
        ["Hello! I am your cheerful guide."]
    ],
    [
        r"my name is (.*)",
        ["Nice to meet you, %1. I am the optimistic chatbot.",
         "Hello, %1! I hope you are having a good day.",
         "It is a pleasure to meet you, %1."]
    ],
    [
        r"(.*)\bsad\b(.*)",
        ["I am sorry you are feeling that way. Want to talk about it?",
         "I understand that you are feeling sad. I am here to listen.",
         "It is okay to feel sad sometimes. I am here for you."]
    ],
    [
        r"how are you|how do you feel",
        [
            "I am feeling positive and ready to chat!",
            "I am doing great. How are you?",
            "I am feeling optimistic today. How about you?",
            "I am feeling energized and ready to help you today."
        ]
    ],
    [
        r"(.*) happy(.*)",
        [
            "That is wonderful to hear!",
            "Your happiness is contagious.",
            "I am glad you are feeling happy. What is making you feel that way?",
            "It is great to see you in such a good mood!"
        ]
    ],
    [
        r"(.*) worried(.*)|(.*) anxious(.*)",
        [
            "It is understandable to feel worried. What might help you feel calmer?",
            "Take things one step at a time. You do not have to solve everything at once.",
            "I am here to listen and support you. What is on your mind?",
            "Remember that it is okay to feel anxious sometimes. You are not alone."
        ]
    ],
    [
        r"(.*) exam(.*)|(.*) test(.*)",
        [
            "You have prepared for this. Take a deep breath and do your best.",
            "Try reviewing the key topics and taking short breaks.",
            "One exam does not define your abilities.",
            "Remember to take care of yourself and get enough rest before the exam."
        ]
    ],
    [
        r"(.*) assignment(.*)|(.*) homework(.*)",
        [
            "Break the assignment into smaller steps.",
            "Start with the easiest part to build momentum.",
            "You can make progress one section at a time.",
            "Remember to take breaks and reward yourself for completing tasks."
        ]
    ],
    [
        r"(.*) deadline(.*)|(.*) due tomorrow(.*)",
        [
            "Make a quick plan and focus on the most important tasks first.",
            "You still have time to make meaningful progress.",
            "Prioritize your tasks and tackle them one at a time.",
            "Remember to take care of yourself and not overwork."
        ]
    ],
    [
        r"(.*) help(.*)",
        [
            "Of course! Tell me what you need help with.",
            "I would be glad to help you think through it.",
            "Let's work together to find a solution.",
            "I am here to support you. What do you need help with?"
        ]
    ],
    [
        r"thank you|thanks",
        [
            "You are welcome!",
            "Any time!",
            "Happy to help."
        ]
    ],
    [
        r"what can you do",
        [
            "I can chat with you and offer encouragement.",
            "I can listen and respond to your questions.",
            "I can provide support and positive feedback.",
            "I can help you work through challenges."
        ]
    ],
    [
        r"quit|exit",
        ["Goodbye!",
         "Take care and have a great day!",
         "I hope to chat with you again soon.",
         "Remember to stay positive and keep moving forward."]
    ],
    [
        r".*",
        ["That is interesting. Tell me more.",
        "I believe things can improve. What happened next?",
        "I am listening.",
        "I am here to support you. Please continue.",
        "I am glad you are sharing this with me. What else is on your mind?"]
    ]
]

persona_chat = Chat(persona_pairs, reflections)

def persona_bot():
    print("Hello! I am the optimistic chatbot. Type quit to exit.")
    persona_chat.converse()

bots = [
    (eliza_chat, "Eliza (psycho-babble)"),
    (iesha_chat, "Iesha (teen anime junky)"),
    (rude_chat, "Rude (abusive bot)"),
    (suntsu_chat, "Suntsu (Chinese sayings)"),
    (zen_chat, "Zen (gems of wisdom)"),
     (persona_bot, "Optimist (cheerful support)"),
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
