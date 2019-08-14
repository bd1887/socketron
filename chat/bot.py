import spacy

class Bot:
    def __init__(self, chat_responses):
        # Load Spacy's English word embeddings
        self.nlp = spacy.load("en_core_web_md")

        # Convert chat responses into Spacy documents
        self.chat_responses = self.prepocess(chat_responses)
        
    def get_response(self, msg):
        if msg:
            # Find the chat response input with greatest similarity to message content
            most_similar_idx = None
            most_similar_score = 0

            # Create Spacy document from message content
            msg_nlp = self.nlp(msg)

            # Iterate through all chat responses
            for idx, chat_response in enumerate(self.chat_responses):

                # Get similarity score from Spacy
                similarity = chat_response.nlp.similarity(msg_nlp)

                # Record most similar
                if similarity > most_similar_score:
                    most_similar_idx = idx
                    most_similar_score = similarity

            # Only respond if highest similarity score is above threshold
            # TODO: Find a reasonable threshold
            if most_similar_score > .6:
                return f'# {self.chat_responses[most_similar_idx].output}'

            if msg == 'Hi, Bot!':
                return '# Hello, Human!'

    # Converts Spacy documents
    def prepocess(self, docs):
        # Arg is single string
        if isinstance(docs, str):
            return self.nlp(docs)

        # Arg is list
        for doc in docs:
            doc.nlp = self.nlp(doc.input)

        return docs