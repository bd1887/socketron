class Bot:
    def __init__(self, chat_responses):
        self.chat_responses = chat_responses

    def get_response(self, msg):
        for chat_response in self.chat_responses:
            if chat_response.input == msg:
                return chat_response.output

        if msg == 'Hi, Bot!':
            return 'Hello, Human!'