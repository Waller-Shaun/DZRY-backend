class QuestionPaser:

    '''构建实体节点'''
    def build_entitydict(self, args):
        entity_dict = {}
        for arg, types in args.items():
            for type in types:
                if type not in entity_dict:
                    entity_dict[type] = [arg]
                else:
                    entity_dict[type].append(arg)

        return entity_dict

    '''解析主函数'''
    def parser_main(self, res_classify):
        args = res_classify['args']
        entity_dict = self.build_entitydict(args)
        question_types = res_classify['question_types']
        sqls = []
        for question_type in question_types:
            sql_ = {}
            sql_['question_type'] = question_type
            sql = []
            if question_type == 'disease_symptom':
                sql = self.sql_transfer(question_type, entity_dict.get('disease'))

            elif question_type == 'symptom_disease':
                sql = self.sql_transfer(question_type, entity_dict.get('symptom'))

            elif question_type == 'symptom_common_disease':
                sql = self.sql_transfer(question_type, entity_dict.get('symptom_common'))

            elif question_type == 'disease_cause':
                sql = self.sql_transfer(question_type, entity_dict.get('disease'))

            elif question_type == 'disease_treatment':
                sql = self.sql_transfer(question_type, entity_dict.get('disease'))

            elif question_type == 'aspect_problem':
                sql = self.sql_transfer(question_type, entity_dict.get('aspect'))

            elif question_type == 'problem_solution':
                sql = self.sql_transfer(question_type, entity_dict.get('problem'))




            if sql:
                sql_['sql'] = sql

                sqls.append(sql_)

        return sqls

    '''针对不同的问题，分开进行处理'''
    def sql_transfer(self, question_type, entities):
        if not entities:
            return []

        # 查询语句
        sql = []
        # 查询疾病的原因
        if question_type == 'disease_cause':
            sql = ["MATCH (m:Disease)-[r:Caused_By]->(n:Pathogen) where m.name = '{0}' return m.name, n.description".format(i)
                   for i in entities]

        # 查询疾病的防治措施
        elif question_type == 'disease_treatment':
            sql = ["MATCH (m:Disease)-[r:Treated_By]->(n:Treatment) where m.name = '{0}' return m.name, n.description".format(i)
                   for i in entities]

        # 查询疾病有哪些症状
        elif question_type == 'disease_symptom':
            sql = ["MATCH (m:Disease)-[r:Has_Symptom]->(n:Symptom) where m.name = '{0}' return m.name, n.description".format(
                i) for i in entities]

        # 查询症状会导致哪些疾病
        elif question_type == 'symptom_disease':
            sql = ["MATCH (m:Disease)-[r:Has_Symptom]->(n:Symptom) where n.description = '{0}' return m.name, n.description".format(i)
                   for i in entities]

        elif question_type == 'symptom_common_disease':
            sql = ["MATCH (m:Disease)-[r:Has_Symptom]->(n:Symptom) where n.name = '{0}' return m.name, n.name".format(i)
                   for i in entities]

        elif question_type == 'aspect_problem':
            sql = ["MATCH (m:Aspect)-[r:Has_Problem]->(n:Problem) where m.description = '{0}' return m.description, n.description".format(i)
                for i in entities]

        elif question_type == 'problem_solution':
            sql = ["MATCH (m:Problem)-[r:Solved_By]->(n:Solution) where m.description = '{0}' return m.description, n.description".format(i)
                for i in entities]

        return sql



if __name__ == '__main__':
    handler = QuestionPaser()




