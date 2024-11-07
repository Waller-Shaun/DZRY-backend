import  os
import  ahocorasick

class QuestionClassifier:
    def __init__(self):
        cur_dir = os.path.dirname(os.path.abspath(__file__))

        #　特征词路径
        self.disease_path = os.path.join(cur_dir, 'dic/disease.txt')
        self.symptom_path = os.path.join(cur_dir, 'dic/symptom.txt')
        self.symptom_common_path = os.path.join(cur_dir, 'dic/symptom_common.txt')
        self.treatment_path = os.path.join(cur_dir, 'dic/treatment.txt')
        self.pathogen_path = os.path.join(cur_dir, 'dic/pathogen.txt')
        self.deny_path = os.path.join(cur_dir, 'dic/deny.txt')
        self.problem_path = os.path.join(cur_dir, 'dic/problem.txt')
        self.aspect_path = os.path.join(cur_dir, 'dic/aspect.txt')
        self.solution_path = os.path.join(cur_dir, 'dic/solution.txt')

        # 加载特征词
        self.disease_wds = [i.strip() for i in open(self.disease_path, encoding='utf-8') if i.strip()]
        self.treatment_wds = [i.strip() for i in open(self.treatment_path, encoding='utf-8') if i.strip()]
        self.pathogen_wds = [i.strip() for i in open(self.pathogen_path, encoding='utf-8') if i.strip()]
        self.symptom_wds = [i.strip() for i in open(self.symptom_path,encoding='utf-8') if i.strip()]
        self.symptom_common_wds = [i.strip() for i in open(self.symptom_common_path, encoding='utf-8') if i.strip()]
        self.aspect_wds = [i.strip() for i in open(self.aspect_path, encoding='utf-8') if i.strip()]
        self.problem_wds = [i.strip() for i in open(self.problem_path, encoding='utf-8') if i.strip()]
        self.solution_wds = [i.strip() for i in open(self.solution_path, encoding='utf-8') if i.strip()]
        self.region_words = set(self.pathogen_wds + self.disease_wds + self.treatment_wds +self.symptom_common_wds+
                                self.symptom_wds + self.aspect_wds + self.problem_wds + self.solution_wds)
        self.deny_words = [i.strip() for i in open(self.deny_path, encoding='utf-8') if i.strip()]
        # 构造领域actree
        self.region_tree = self.build_actree(list(self.region_words))
        # 构建词典
        self.wdtype_dict = self.build_wdtype_dict()
        # 问句疑问词
        self.symptom_qwds = ['症状', '表征', '现象', '症候', '表现']
        self.cause_qwds = ['原因','成因', '为什么', '怎么会', '怎样才', '咋样才', '怎样会', '如何会',
                           '为啥', '为何', '如何才会','怎么才会', '会导致', '会造成', '为什么']
        self.treatment_qwds = ['预防', '防范', '抵制', '抵御', '防止','躲避','逃避','避开','免得','逃开',
                             '避开','避掉','躲开','躲掉','绕开','怎样才能不', '怎么才能不', '咋样才能不',
                             '咋才能不', '如何才能不','怎样才不', '怎么才不', '咋样才不','咋才不', '如何才不',
                             '怎样才可以不', '怎么才可以不', '咋样才可以不', '咋才可以不', '如何可以不','怎样才可不',
                             '怎么才可不', '咋样才可不', '咋才可不', '如何可不','怎么治疗', '如何医治', '怎么医治',
                             '怎么治', '怎么医', '如何治','医治方式', '疗法', '咋治', '怎么办', '咋办', '咋治','怎么解决',
                             '怎么处理','怎么克服','解决办法','改善','有哪些处理方案','有哪些解决方案','怎么应对','如何化解',
                             '怎么排除','如何排除','如何处理','如何解决','如何客服','有什么应对措施',]
        self.test_qwds = ['sb']
        self.problem_qwds = ['会出现','有哪些','常见','面临','是什么','注意','发生','带来','影响','困难','会导致', '会造成','会发生']

        return

        '主函数部分：'

        '''基于特征词进行分类'''

    def check_words(self, wds, sent):
        for wd in wds:
            if wd in sent:
                return True
        return False

        '''构造actree，加速过滤'''

    def build_actree(self, wordlist):
        actree = ahocorasick.Automaton()
        for index, word in enumerate(wordlist):
            actree.add_word(word, (index, word))
        actree.make_automaton()
        return actree

        '''问句过滤'''

    def check_medical(self, question):
        region_wds = []
        for i in self.region_tree.iter(question):
            wd = i[1][1]
            region_wds.append(wd)
        stop_wds = []
        for wd1 in region_wds:
            for wd2 in region_wds:
                if wd1 in wd2 and wd1 != wd2:
                    stop_wds.append(wd1)
        final_wds = [i for i in region_wds if i not in stop_wds]
        final_dict = {i: self.wdtype_dict.get(i) for i in final_wds}

        return final_dict

        '''构造词对应的类型'''

    def build_wdtype_dict(self):
        wd_dict = dict()
        for wd in self.region_words:
            wd_dict[wd] = []
            if wd in self.disease_wds:
                wd_dict[wd].append('disease')
            if wd in self.pathogen_wds:
                wd_dict[wd].append('pathogen')
            if wd in self.treatment_wds:
                wd_dict[wd].append('treatment')
            if wd in self.symptom_wds:
                wd_dict[wd].append('symptom')
            if wd in self.symptom_common_wds:
                wd_dict[wd].append('symptom_common')
            if wd in self.aspect_wds:
                wd_dict[wd].append('aspect')
            if wd in self.problem_wds:
                wd_dict[wd].append('problem')
            if wd in self.solution_wds:
                wd_dict[wd].append('solution')
        return wd_dict

        '''分类主函数'''

    def classify(self, question):
        data = {}
        medical_dict = self.check_medical(question)
        if not medical_dict:
            return {}
        data['args'] = medical_dict
        # 收集问题当中所涉及到的实体类型
        types = []
        for each in medical_dict.values():
            types.extend(each)
        question_type = 'others'

        question_types = []

        #  疾病症状
        if self.check_words(self.symptom_qwds, question) and ('disease' in types):
            question_type = 'disease_symptom'
            question_types.append(question_type)

        if self.check_words(self.test_qwds, question) and ('symptom' in types):
            question_type = 'symptom_disease'
            question_types.append(question_type)

        # 多种疾病共有的特征的问句类型
        if self.check_words(self.cause_qwds, question) and ('symptom_common' in types):
            question_type = 'symptom_common_disease'
            question_types.append(question_type)

        #  疾病原因
        if self.check_words(self.cause_qwds, question) and ('disease' in types):
            question_type = 'disease_cause'
            question_types.append(question_type)


        # 　疾病症状防治疗
        if self.check_words(self.treatment_qwds, question) and 'disease' in types:
            question_type = 'disease_treatment'
            question_types.append(question_type)

        #  养殖问题
        if self.check_words(self.problem_qwds, question) and ('aspect' in types):
            question_type = 'aspect_problem'
            question_types.append(question_type)

        # 养殖问题解决
        if self.check_words(self.treatment_qwds, question) and ('problem' in types):
            question_type = 'problem_solution'
            question_types.append(question_type)

        # 若没有查到相关的外部查询信息，那么则将该疾病的描述信息返回
        if question_types == [] and 'disease' in types:
            question_types = ['disease_desc']

        # 若没有查到相关的外部查询信息，那么则将该疾病的描述信息返回
        if (question_types == []):
            if('symptom' in types):
                question_types = ['symptom_disease']
            elif('symptom_common' in types):
                question_types = ['symptom_common_disease']


        # 将多个分类结果进行合并处理，组装成一个字典
        data['question_types'] = question_types

        return data


if __name__ == '__main__':
    handler = QuestionClassifier()
    while 1:
        question = input('input an question:')
        data = handler.classify(question)
        print(data)
