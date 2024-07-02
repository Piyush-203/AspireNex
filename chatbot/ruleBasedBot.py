import random
import re

class RuleBasedBot:
    # Negative responses
    neg_responses = ("no", "nope", "nah", "not a chance", "sorry")

    # Exit commands for stopping the conversation
    exit_cmds = ("quit", "pause", "exit", "goodbye", "bye", "later", "stop", "thank you")

    def __init__(self):
        # Rules for the bot (dictionary)
        self.bot_responses = {
            'ask_about_product': r'\bproduct\b',
            'technical_support': r'\btechnical\b|\bsupport\b',
            'about_returns': r'\breturn policy\b',
            'general_query': r'\bhow\b|\bhelp\b'
        }

    def greeting(self):
        self.name = input("Hello! Welcome to our support. What's your name?\n")
        help_response = input(f"Hello {self.name}! How can I help you today? Enter to continue\n").lower()
        
        if help_response in self.neg_responses:
            print("Alright, have a great day!")
            return
        self.chat()

    def make_exit(self, reply):
        for cmd in self.exit_cmds:
            if cmd in reply:
                print("Thanks for reaching out, have a great day!")
                return True
        return False

    def chat(self):
        reply = input("Please tell me your query: ").lower()
        while not self.make_exit(reply):
            reply = input(f'{self.match_reply(reply)}\n Query: ').lower()

    def match_reply(self, reply):
        for intent, regex_pat in self.bot_responses.items():
            found_match = re.search(regex_pat, reply)
            if found_match:
                if intent == 'ask_about_product':
                    return self.ask_about_product()
                elif intent == 'technical_support':
                    return self.technical_support()
                elif intent == 'about_returns':
                    return self.about_returns()
                elif intent == 'general_query':
                    return self.general_query()
        return self.no_match_intent()

    def ask_about_product(self):
        response = (
            "Our product is top-notch and has excellent reviews!\n",
            "You can find all the product details on our website.\n"
        )
        return random.choice(response)

    def technical_support(self):
        response = (
            "Please visit our technical support page for detailed assistance.\n",
            "Our technical support team is available 24/7 to assist you. You can contact us at xyz.\n",
            "You can also call our tech support helpline for immediate help.\n"
        )
        return random.choice(response)

    def about_returns(self):
        response = (
            "We have a 30-day return policy for all our products.\n",
            "If you are not satisfied with your purchase, you can return it within 30 days of the purchase date.\n",
            "Please contact our customer support team for more details on our return policy.\n",
            "Please ensure the product is in its original condition when returning.\n"
        )
        return random.choice(response)

    def general_query(self):
        response = (
            "How can I assist you further?\n",
            "Please let me know if you have any other queries.\n",
            "I am here to help you with any queries you may have.\n"
        )
        return random.choice(response)

    def no_match_intent(self):
        response = (
            "I am sorry, I did not understand your query.\n",
            "Please rephrase your query.\n",
            "I am not sure I understood your query.\n",
            "I am sorry, I am not able to assist you with that.\n"
        )
        return random.choice(response)

bot = RuleBasedBot()
bot.greeting()
