import spacy


class TextAnalyzer:
    nlp = spacy.load('en_core_web_sm')
    def get_noun_subject(self, token, count=3):
        current_head = token.head
        while token != current_head:
            # print(current_head)
            if current_head.pos_ == 'NOUN':
                return current_head
            current_head = current_head.head
            count-=1
            if count==0:
                return token
        return token

    def get_verb_subject(self, doc, count=3):
        # possible_subjects = []
        for word in doc:
            if word.pos_ == 'VERB':
                modifier = self.get_adj_from_parent(word)
                if modifier:
                    # possible_subjects.append((modifier, word))
                    return (modifier, word.text)
        return []
        # return possible_subjects

    def get_adj_from_children(self, token, count=2):
        all_children = list(token.children)
        possible_adj = ''
        for child in all_children:
            if child.pos_ == 'NOUN' and possible_adj == '':
                possible_adj = self.get_adj_from_children(child)
            elif child.pos_ == 'ADJ':
                return child.text
        return possible_adj

    def get_adj_from_parent(self, token, count=2):
        head = token.head
        if head.pos_ == 'ADJ':
            return head.text
        all_children = list(head.children)
        for child in all_children:
            if child.pos_ == 'ADJ':
                return child.text
        if count-1==0:
            return ''
        return self.get_adj_from_parent(head, count=count-1)
    
    def get_adjlike_from_parent(self, token, doc, count=2):

        def get_meaningful_token(tok, doc):
            children = list(tok.children)
            index_marker = tok.i
            for child in children:
                if child.pos_ in considered_child_pos:
                    if abs(tok.i-index_marker)<abs(tok.i-child.i) and abs(tok.i-child.i)<5:
                        index_marker = child.i
            if tok.i != index_marker:
                start, end = (tok.i, index_marker +1) if tok.i<index_marker else (index_marker, tok.i+1)
                return doc[start:end].text
            return tok.text

        head = token.head
        considered_pos = ('VERB', 'ADV')
        considered_child_pos = ('ADV', 'ADP')
        if head.pos_ in considered_pos:
            return get_meaningful_token(head, doc)
        all_children = list(head.children)
        for child in all_children:
            if child.pos_ in considered_pos:
                return get_meaningful_token(child, doc)
        if count-1==0:
            return ''
        return self.get_adjlike_from_parent(head, doc, count = count-1)

    def extract_subject(self, text):
        doc = self.nlp(text)
        possible_subjects = []
        subject = ''
        subject_length = 0
        for token in doc:
            if token.pos_ == 'NOUN':
                # print('\n',token)
                head = self.get_noun_subject(token)
                modifier = self.get_adj_from_children(head)
                if not modifier:
                    modifier = self.get_adj_from_parent(head)
                if not modifier:
                    modifier = self.get_adjlike_from_parent(head, doc)
                start, end= (head.i, token.i+1) if head.i<=token.i else (token.i, head.i+1)
                if any([tok.is_digit for tok in doc[start:end]]):
                    continue
                possible_subjects.append((modifier, doc[start:end].text))
                if end-start>subject_length:
                    subject_length = end-start
                    subject = possible_subjects[-1]
        
        # if not subject:
        #     return self.get_verb_subject(doc)
        return ' '.join(subject)
