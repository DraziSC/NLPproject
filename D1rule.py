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
        r"I am (\d+) years? old",
        [
            "It is nice to meet you! Being %1 years old is a great stage of life.",
            "Thanks for telling me. You have plenty of opportunities ahead of you.",
            "I hope you are enjoying being %1 years old and making the most of it.",
            "Age is just a number, but the experiences you gain are invaluable."
        ]
    ],
    [
        r"(?:I live in|I am from) (.*)",
        [
            "That sounds interesting. What do you like most about %1?",
            "Thanks for sharing that with me.",
            "I hope you are enjoying your time in %1 and making the most of it.",
            "It is great to hear that you are from %1. What is your favorite thing about it?"
        ]
    ],
    [
        r"(?:I study|I work as) (.*)",
        [
            "That sounds interesting! What do you enjoy most about %1?",
            "I hope you are enjoying %1 and making progress toward your goals.",
            "It is great to see you pursuing your studies or career in %1.",
            "I am proud of you for choosing %1 as your path."
        ]
    ],
    [
        r"(?:my hobby is|I like) (.*)",
        [
            "%1 sounds like a great interest! Tell me more about it.",
            "That is wonderful. Hobbies can be a great way to relax and grow.",
            "I am glad you have a hobby like %1. What do you enjoy most about it?",
            "It is great to hear that you enjoy %1. How did you get started with it?"
        ]
    ],
    [
        r"(.*)\bsad(.*)",
        ["I am sorry you are feeling that way. Want to talk about it?",
         "I understand that you are feeling sad. I am here to listen.",
         "It is okay to feel sad sometimes. I am here for you.",
         "Remember that it is okay to express your feelings. I am here to support you."]
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
            "Happy to help.",
            "I am glad I could support you."
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
        r"what should I do|what do you suggest|can you give me advice",
        [
            "Start with one small step and build from there.",
            "Consider your options and choose the next action that feels manageable.",
            "Make a short plan, then focus on the most important task first.",
            "Remember to take care of yourself and not overwork."
        ]
    ],
    [
        r"why am I stressed|why do I feel stressed|why am I worried",
        [
            "Stress can build up when you have too many things to manage at once.",
            "It may help to identify what is worrying you and deal with one part at a time.",
            "Take a breath and think about what you can control right now.",
            "Remember to take breaks and practice self-care to reduce stress."
        ]
    ],
    [
        r"how can I improve|how can I get better|how do I succeed",
        [
            "Set a clear goal and make steady progress toward it.",
            "Learn from mistakes, keep practicing, and celebrate small improvements.",
            "Ask for feedback and use it to decide what to try next.",
            "Stay positive and keep moving forward, even if progress is slow."
        ]
    ],
    [
        r"I cannot do it|I can't do it|this is too hard|I want to give up|I need motivation|I feel unmotivated",
        [
            "You do not have to do everything at once. Start with one small step.",
            "Difficult does not mean impossible. Keep going at your own pace.",
            "Take a short break, then try the next manageable part.",
            "You have overcome difficult things before, and you can make progress here too."
        ]
    ],
    [
        r"you are (nice|kind|helpful|great|amazing)|good chatbot|I like talking to you",
        [
            "Thank you! I am happy that I can support you.",
            "That is kind of you to say. I enjoy talking with you too.",
            "Thank you! Your positive words made my day.",
            "I am glad you are enjoying our conversation. I am here to help."
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
