from py2neo import Graph

class AnswerSearcher:
    def __init__(self):
        self.g = Graph("bolt://localhost:7687", auth=("neo4j", "040426Kk"))
        self.num_limit = 100

    '''执行cypher查询，并返回相应结果'''
    def search_main(self, sqls):
        final_answers = []
        for sql_ in sqls:
            question_type = sql_['question_type']
            queries = sql_['sql']
            answers = []
            for query in queries:
                ress = self.g.run(query).data()
                answers += ress
            final_answer = self.answer_prettify(question_type, answers)
            if final_answer:
                final_answers.append(final_answer)
        return final_answers

    '''根据对应的qustion_type，调用相应的回复模板'''
    def answer_prettify(self, question_type, answers):
        final_answer = []
        if not answers:
            return ''
        if question_type == 'disease_symptom':
            desc = [i['n.description'] for i in answers]
            subject = answers[0]['m.name']
            final_answer = '{0}的症状包括：{1}'.format(subject, '；'.join(list(set(desc))[:self.num_limit]))

        elif question_type == 'symptom_disease':
            desc = [i['m.name'] for i in answers]
            subject = answers[0]['n.description']
            final_answer = '症状{0}可能染上的疾病有：{1}'.format(subject, '；'.join(list(set(desc))[:self.num_limit]))

        elif question_type == 'symptom_common_disease':
            desc = [i['m.name'] for i in answers]
            subject = answers[0]['n.name']
            final_answer = '症状{0}可能染上的疾病有：{1}'.format(subject, '；'.join(list(set(desc))[:self.num_limit]))

        elif question_type == 'disease_cause':
            desc = [i['n.description'] for i in answers]
            subject = answers[0]['m.name']
            final_answer = '{0}可能的成因有：{1}'.format(subject, '；'.join(list(set(desc))[:self.num_limit]))

        elif question_type == 'disease_treatment':
            desc = [i['n.description'] for i in answers]
            subject = answers[0]['m.name']
            final_answer = '{0}的预防措施包括：{1}'.format(subject, '；'.join(list(set(desc))[:self.num_limit]))

        elif question_type == 'aspect_problem':
            desc = [i['n.description'] for i in answers]
            subject = answers[0]['m.description']
            final_answer = '{0}可能导致的问题有：{1}'.format(subject, '；'.join(list(set(desc))[:self.num_limit]))

        elif question_type == 'problem_solution':
            desc = [i['n.description'] for i in answers]
            subject = answers[0]['m.description']
            final_answer = '{0}的解决措施有：{1}'.format(subject, '；'.join(list(set(desc))[:self.num_limit]))



        return final_answer


if __name__ == '__main__':
    searcher = AnswerSearcher()
