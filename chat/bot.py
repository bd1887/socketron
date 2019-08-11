import spacy

class Bot:
    def __init__(self, chat_responses):
        self.nlp = spacy.load("en_core_web_md")
        self.chat_responses = self.prepocess(chat_responses)
        

    def get_response(self, msg):
        if msg:
            most_similar_idx = None
            most_similar_score = 0
            for idx, chat_response in enumerate(self.chat_responses):
                msg_nlp = self.nlp(msg)
                similarity = chat_response.nlp.similarity(msg_nlp)
                print(f'{msg} | {chat_response.input} | {similarity}')
                if similarity > most_similar_score:
                    most_similar_idx = idx
                    most_similar_score = similarity

            if most_similar_score > .6:
                return self.chat_responses[most_similar_idx].output

            if msg == 'Hi, Bot!':
                return 'Hello, Human!'

    def prepocess(self, docs):
        if isinstance(docs, str):
            return self.nlp(docs)

        for doc in docs:
            doc.nlp = self.nlp(doc.input)

        return docs