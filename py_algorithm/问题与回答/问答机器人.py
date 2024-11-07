import sys
import io

from 问题特征提取 import *
from 根据特征查询知识图谱 import *
from 形成回答 import *

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

'''问答类'''
class ChatBotGraph:
    def __init__(self):
        self.classifier = QuestionClassifier()
        self.parser = QuestionPaser()
        self.searcher = AnswerSearcher()

    def chat_main(self, sent):
        answer = '您好，我是大智若渔智能助理，希望可以帮到您。如果没答上来，可联系尼玛。祝您身体棒棒！'
        res_classify = self.classifier.classify(sent)
        if not res_classify:
            return answer
        res_sql = self.parser.parser_main(res_classify)
        final_answers = self.searcher.search_main(res_sql)
        if not final_answers:
            return answer
        else:
            return '\n'.join(final_answers)

if __name__ == '__main__':
    #print("Received input:", sys.argv[1])
    handler = ChatBotGraph()

    input_text = sys.argv[1]
    #question = input('用户:')
    answer = handler.chat_main(input_text)
    result = '小渔:' + answer
    print(result)