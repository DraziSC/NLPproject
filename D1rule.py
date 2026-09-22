import random
import spacy

nlp = spacy.load("en_core_web_sm")

# ==============================================================================
# Lemmatization Preprocessing:
# Lemmatization reduces words to their canonical base form (lemma) using spaCy's
# pre-trained English model (en_core_web_sm). Unlike rule-based stemming which
# blindly chops off suffixes, spaCy uses part-of-speech (POS) tagging and vocabulary
# lookup tables to accurately determine root lemmas based on sentence context:
#
# How it works in this pipeline:
#   1. doc = nlp(text): Tokenizes the user text and runs POS tagging & morphological
#      analysis on each token.
#   2. token.lemma_.lower(): Retrieves the canonical base lemma for each word and
#      normalizes it to lowercase for case-insensitive regex matching.
#      Examples:
#        - Inflected verbs: "am", "is", "are", "'m", "'re" -> "be"
#        - Gerunds/past tenses: "studying", "studied" -> "study"
#        - Plural nouns: "exams" -> "exam", "hobbies" -> "hobby"
#        - Irregulars: "better" -> "well"
#   3. not token.is_punct: Filters out punctuation tokens (e.g., ",", ".", "!") so
#      they do not interfere with regex word boundaries (\b).
#   4. " ".join(...): Reassembles the filtered lemmas into a single whitespace-
#      delimited string ready for pattern matching against persona_pairs.
#
# This drastically simplifies regex rules by matching base lemmas rather than
# having to write exhaustive patterns for every verb tense and noun inflection.
# ==============================================================================
def lemmatize_text(text):
    doc = nlp(text)
    return " ".join([token.lemma_.lower() for token in doc if not token.is_punct])

# function to remove stop words from users input
def remove_stopwords(text):
    doc = nlp(text)
    filtered_tokens = [token.text for token in doc if not token.is_stop and not token.is_punct]
    return " ".join(filtered_tokens)

# function to extract key topics (nouns / proper nouns) using spaCy NLP pipeline
def extract_key_topics(text):
    doc = nlp(text)
    nouns = [token.text for token in doc if not token.is_stop and not token.is_punct and token.pos_ in ("NOUN", "PROPN")]
    if nouns:
        return ", ".join(nouns)
    # fallback to all non-stopwords
    return remove_stopwords(text)

# function to generate intelligent fallback response using extracted content/topic words
def generate_fallback_response(topic):
    if not topic:
        return random.choice([
            "I am listening. Tell me more about what is on your mind.",
            "I am here to support you. Please go ahead.",
            "Take your time. What would you like to talk about?",
            "I am here for you. How can I help today?"
        ])

    templates = [
        f"You mentioned '{topic}'. Tell me more about that.",
        f"What specifically about '{topic}' is on your mind?",
        f"I hear you talking about '{topic}'. How does that make you feel?",
        f"Thanks for sharing that. How is '{topic}' affecting your day?",
        f"I believe things can improve with '{topic}'. What do you want to talk about next?"
    ]
    return random.choice(templates)


"""
A class for simple chatbots.  These perform simple pattern matching on sentences
typed by users, and respond with automatically generated sentences.
"""

from nltk.chat.util import Chat, reflections

# Initialize the persona chatbot with a set of patterns and responses. Each pattern is a regular expression that matches user input, 
# and the corresponding responses are templates that can include captured groups from the input.
persona_pairs = [
    [
        r".*\bmy name (?:is|be|'s) (.*)",
        ["Nice to meet you, %1. I am the optimistic chatbot.",
         "Hello, %1! I hope you are having a good day.",
         "It is a pleasure to meet you, %1."]
    ],
    [
        r"^(?:hello|hi|hey)(?:\s+there)?\b[\s!.]*$|^good\s+(?:morning|afternoon|evening)\b.*",
        ["Hello! I am your cheerful guide."]
    ],
    [
        r".*\bi (?:am|be) (\d+)(?:\s+year(?:s)?\s+old)?\b.*",
        [
            "It is nice to meet you! Being %1 years old is a great stage of life.",
            "Thanks for telling me. You have plenty of opportunities ahead of you.",
            "I hope you are enjoying being %1 years old and making the most of it.",
            "Age is just a number, but the experiences you gain are invaluable."
        ]
    ],
    [
        r".*\b(?:i live in|i (?:am|be) from) (.*)",
        [
            "That sounds interesting. What do you like most about %1?",
            "Thanks for sharing that with me.",
            "I hope you are enjoying your time in %1 and making the most of it.",
            "It is great to hear that you are from %1. What is your favorite thing about it?"
        ]
    ],
    [
        r".*\b(?:you (?:are|be) (?:very\s+|so\s+|really\s+)?(?:nice|kind|helpful|great|amazing)|good chatbot|i like (?:talking|talk) to you)\b.*",
        [
            "Thank you! I am happy that I can support you.",
            "That is kind of you to say. I enjoy talking with you too.",
            "Thank you! Your positive words made my day.",
            "I am glad you are enjoying our conversation. I am here to help."
        ]
    ],
    [
        r".*\b(?:i (?:be\s+)?(?:study|work as|work in))\s+(.*)",
        [
            "That sounds interesting! What do you enjoy most about %1?",
            "I hope you are enjoying %1 and making progress toward your goals.",
            "It is great to see you pursuing your studies or career in %1.",
            "I am proud of you for choosing %1 as your path."
        ]
    ],
    [
        r".*\b(?:my hobby (?:is|be)|i like) (.*)",
        [
            "%1 sounds like a great interest! Tell me more about it.",
            "That is wonderful. Hobbies can be a great way to relax and grow.",
            "I am glad you have a hobby like %1. What do you enjoy most about it?",
            "It is great to hear that you enjoy %1. How did you get started with it?"
        ]
    ],
    [
        r".*\b(?:how (?:are|be) you|how do you feel)\b.*",
        [
            "I am feeling positive and ready to chat!",
            "I am doing great. How are you?",
            "I am feeling optimistic today. How about you?",
            "I am feeling energized and ready to help you today."
        ]
    ],
    [
        r".*\bwhat can you do\b.*",
        [
            "I can chat with you and offer encouragement.",
            "I can listen and respond to your questions.",
            "I can provide support and positive feedback.",
            "I can help you work through challenges."
        ]
    ],
    [
        r".*\b(?:what should i do|what do you suggest|can you give (?:me|i) advice)\b.*",
        [
            "Start with one small step and build from there.",
            "Consider your options and choose the next action that feels manageable.",
            "Make a short plan, then focus on the most important task first.",
            "Remember to take care of yourself and not overwork."
        ]
    ],
    [
        r".*\bhow (?:can|do) i (?:improve|get (?:better|well)|succeed)\b.*",
        [
            "Set a clear goal and make steady progress toward it.",
            "Learn from mistakes, keep practicing, and celebrate small improvements.",
            "Ask for feedback and use it to decide what to try next.",
            "Stay positive and keep moving forward, even if progress is slow."
        ]
    ],
    [
        r".*\b(?:why (?:am|be) i (?:stressed|stress)|why do i feel (?:stressed|stress)|why (?:am|be) i (?:worried|worry))\b.*",
        [
            "Stress can build up when you have too many things to manage at once.",
            "It may help to identify what is worrying you and deal with one part at a time.",
            "Take a breath and think about what you can control right now.",
            "Remember to take breaks and practice self-care to reduce stress."
        ]
    ],
    [
        r".*\bi (?:am|be|feel|be\s+feel)\s+(?:stressed|stress)\b.*",
        [
            "I am sorry you are feeling stressed. Take a deep breath and take things one step at a time.",
            "It is okay to feel stressed sometimes. Remember to take breaks and be kind to yourself.",
            "Stress can feel overwhelming. What is the main thing causing you stress right now?",
            "Take a moment to pause. You do not have to solve everything right this second."
        ]
    ],
    [
        r".*\b(?:not|never)\s+(?:(?:feel|be)\s+)?(?:very\s+|so\s+|that\s+|too\s+)?sad\b.*",
        [
            "I am glad to hear that you are not feeling sad.",
            "That is good to hear! What is on your mind today?",
            "I am pleased to hear that. How are things going for you?"
        ]
    ],
    [
        r".*\bsad\b.*",
        ["I am sorry you are feeling that way. Want to talk about it?",
         "I understand that you are feeling sad. I am here to listen.",
         "It is okay to feel sad sometimes. I am here for you.",
         "Remember that it is okay to express your feelings. I am here to support you."]
    ],
    [
        r".*\b(?:(?:not|never)\s+(?:(?:feel|be|do)\s+)?(?:very\s+|so\s+|that\s+|too\s+)?(?:happy|good|well|okay|great)|unhappy)\b.*",
        [
            "I am sorry to hear you are not feeling happy. What has been on your mind?",
            "It is completely okay not to feel okay. I am here to listen whenever you want to talk.",
            "Take things one moment at a time. Even tough days can get better.",
            "I am here to support you. Would you like to talk about what is bothering you?",
            "Be kind to yourself today. Remember that difficult feelings will pass."
        ]
    ],
    [
        r".*\bhappy\b.*",
        [
            "That is wonderful to hear!",
            "Your happiness is contagious.",
            "I am glad you are feeling happy. What is making you feel that way?",
            "It is great to see you in such a good mood!"
        ]
    ],
    [
        r".*\b(?:not|never)\s+(?:(?:feel|be)\s+)?(?:very\s+|so\s+|that\s+|too\s+)?(?:worried|worry|anxious|anxiety)\b.*",
        [
            "I am glad you are feeling calm and not worried.",
            "That is wonderful to hear! A calm mind is a great foundation.",
            "I am happy to hear that. What would you like to talk about today?"
        ]
    ],
    [
        r".*\b(?:worried|worry|anxious|anxiety)\b.*",
        [
            "It is understandable to feel worried. What might help you feel calmer?",
            "Take things one step at a time. You do not have to solve everything at once.",
            "I am here to listen and support you. What is on your mind?",
            "Remember that it is okay to feel anxious sometimes. You are not alone."
        ]
    ],
    [
        r".*\b(?:exam|test)\b.*",
        [
            "You have prepared for this. Take a deep breath and do your best.",
            "Try reviewing the key topics and taking short breaks.",
            "One exam does not define your abilities.",
            "Remember to take care of yourself and get enough rest before the exam."
        ]
    ],
    [
        r".*\b(?:assignment|homework)\b.*",
        [
            "Break the assignment into smaller steps.",
            "Start with the easiest part to build momentum.",
            "You can make progress one section at a time.",
            "Remember to take breaks and reward yourself for completing tasks."
        ]
    ],
    [
        r".*\b(?:deadline|due\s+(?:tomorrow|today|soon|next\s+week))\b.*",
        [
            "Make a quick plan and focus on the most important tasks first.",
            "You still have time to make meaningful progress.",
            "Prioritize your tasks and tackle them one at a time.",
            "Remember to take care of yourself and not overwork."
        ]
    ],
    [
        r".*\b(?:i can not do it|.*too hard|i want to give up|i need motivation|i feel unmotivated)\b.*",
        [
            "You do not have to do everything at once. Start with one small step.",
            "Difficult does not mean impossible. Keep going at your own pace.",
            "Take a short break, then try the next manageable part.",
            "You have overcome difficult things before, and you can make progress here too."
        ]
    ],
    [
        r".*\bhelp\b.*",
        [
            "Of course! Tell me what you need help with.",
            "I would be glad to help you think through it.",
            "Let's work together to find a solution.",
            "I am here to support you. What do you need help with?"
        ]
    ],
    [
        r".*\b(?:thank\s+you|thank(?:s)?)\b.*",
        [
            "You are welcome!",
            "Any time!",
            "Happy to help.",
            "I am glad I could support you."
        ]
    ],
    [
        r"^(?:quit|exit|bye|goodbye)$",
        ["Goodbye!",
         "Take care and have a great day!",
         "I hope to chat with you again soon.",
         "Remember to stay positive and keep moving forward."]
    ]
]

# NLTK's Chat engine uses the 'reflections' dictionary to swap 1st and 2nd person
# pronouns and verbs when echoing captured wildcards (%1, %2, etc.) back to the user
# (e.g., transforming "my" -> "your", "I am" -> "you are").
#
# Standard NLTK reflections only cover inflected surface forms like "i am" and "you are".
# However, because we preprocess user input with spaCy lemmatization (lemmatize_text),
# verbs like "am", "is", and "are" are normalized to their base lemma "be" (e.g., "i be").
#
# Without these custom additions:
# 1. "i be" would not be recognized by NLTK and would echo back awkwardly as "i be".
# 2. spaCy sometimes lemmatizes "me" to the base pronoun "i", so explicit mappings
#    ensure proper pronoun reflection back to natural conversational English.
custom_reflections = dict(reflections)
custom_reflections.update({
    "i be": "you are",
    "you be": "I am",
    "i": "you",
    "me": "you",
    "my": "your",
    "your": "my"
})

# Initialize the persona chat with the custom reflections
persona_chat = Chat(persona_pairs, custom_reflections)

ASCII_BANNER = r"""
=======================================================================
          \   |   /       ___        _   _           _     _   
           .-'''-.       / _ \ _ __ | |_(_)_ __ ___ (_)___| |_ 
        -=(  ^_^  )=-   | | | | '_ \| __| | '_ ` _ \| / __| __|
           '-...-'      | |_| | |_) | |_| | | | | | | \__ \ |_ 
          /   |   \      \___/| .__/ \__|_|_| |_| |_|_|___/\__|
                              |_|                              
                 ~ Cheerful Support & Positivity ~
=======================================================================
"""

# Create a function to run the persona chatbot
def persona_bot():
    print(ASCII_BANNER)
    print("Hello! I am the optimistic chatbot. Type quit to exit.\n")
    while True:
        try:
            user_input = input(">")
        except EOFError:
            print("quit")
            break

        user_input = user_input.strip()
        if not user_input:
            continue

        #print(f"User input: {user_input}")  # Debugging line to print user input

        key_topics = extract_key_topics(user_input)
        #print(f"Key topics extracted (POS NOUN/PROPN): {key_topics}")  # Debugging line

        lemmatized_input = lemmatize_text(user_input)
        #print(f"User input after lemmatization: {lemmatized_input}")  # Debugging line

        clean_input = lemmatized_input.strip()
        while clean_input and clean_input[-1] in "!.?":
            clean_input = clean_input[:-1].strip()

        if not clean_input:
            continue

        response = persona_chat.respond(clean_input)
        if response is None:
            response = generate_fallback_response(key_topics)

        print(response)

        if clean_input.lower() in ["quit", "exit", "bye", "goodbye"]:
            break


if __name__ == "__main__":
    persona_bot()
