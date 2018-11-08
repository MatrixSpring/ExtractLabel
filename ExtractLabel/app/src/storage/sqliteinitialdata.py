import sqlite3


class SqlitePersist(object):

    def __init__(self):
        self.db = None

    def connect(self):
        try:
            self.db = sqlite3.connect("Sqlite3DB.db")
            sql_create_table = """CREATE TABLE IF NOT EXISTS `UserTable` (
                                                `id` INTEGER PRIMARY KEY AUTOINCREMENT,
                                                `created` CHAR(256) NOT NULL,
                                                `custom_id` CHAR(256) NOT NULL,
                                                `note_id` CHAR(256) NOT NULL,
                                                `user_id` CHAR(256) NOT NULL, 
                                                `remarks` TEXT,
                                                `class_type` CHAR(256), 
                                                `keyword` CHAR(512), 
                                                `neo4j_id` CHAR(512), 
                                                `score` CHAR(256)
                                                 )"""
            self.db.execute(sql_create_table)
        except Exception as e:
            print("sqlite3 connect failed." + str(e))

    def close(self):
        try:
            if self.db is not None:
                self.db.close()
        except BaseException as e:
            print("sqlite3 close failed." + str(e))

    def insert_table_dict(self, dict_data=None):
        if dict_data is None:
            return False
        try:
            cols = ', '.join(list(dict_data.keys()))
            values = '"," '.join(list(dict_data.values()))
            sql_insert = "INSERT INTO `UserTable`(%s) VALUES (%s)" % (cols, '"' + values + '"')
            self.db.execute(sql_insert)
            self.db.commit()
        except BaseException as e:
            self.db.rollback()
        return True

    def get_dict_by_custom_id(self, name=None):
        if name is None:
            sql_select_table = "SELECT * FROM `UserTable`"
        else:
            sql_select_table = "SELECT * FROM `UserTable` WHERE custom_id==%s" % ('"' + name + '"')
        cursor = self.db.execute(sql_select_table)
        ret_list = list()
        for row in cursor:
            ret_list.append({'id': row[0], 'created': row[1], 'custom_id': row[2], 'note_id': row[3], 'user_id': row[4],
                             'remarks': row[5]})
        return ret_list

    def update_cols_category_dict(self, dict_data=None):
        if dict_data is None:
            return False
        try:
            # UPDATE 表名称 SET 列名称 = 新值 WHERE 列名称 = 某值
            sql_insert = "UPDATE `UserTable` SET class_type=%s WHERE created=%s" % (
                '"' + dict_data['class_type'] + '"', '"' + str(dict_data['created']) + '"')
            print('sql_insert : ', sql_insert)
            self.db.execute(sql_insert)
            self.db.commit()
        except BaseException as e:
            print('sql_insert BaseException : ', e)
            self.db.rollback()
        return True

    def insert_table_dict_transform(self, dict_data=None):
        item_data = {'created': str(dict_data['created']), 'custom_id': dict_data['custom_id'],
                     'note_id': dict_data['note_id'], 'user_id': dict_data['user_id'], 'remarks': dict_data['remarks']}
        self.insert_table_dict(item_data)

    def get_dict_all_data(self):
        sql_select_table = "SELECT * FROM `UserTable`"
        cursor = self.db.execute(sql_select_table)
        ret_list = list()
        for row in cursor:
            ret_list.append({'id': row[0], 'created': row[1], 'custom_id': row[2], 'note_id': row[3], 'user_id': row[4],
                             'remarks': row[5], 'class_type': row[6]})
        return ret_list

    def get_dict_all_content(self):
        sql_select_table = "SELECT * FROM `UserTable`"
        cursor = self.db.execute(sql_select_table)
        ret_list = list()
        for row in cursor:
            ret_list.append(row[5])
        return ret_list

    def get_category_data(self):
        sql_select_table = "SELECT class_type, count(class_type) AS number FROM `UserTable` group by class_type"
        print('sql_select_table : ', sql_select_table)
        cursor = self.db.execute(sql_select_table)
        ret_list = list()
        for row in cursor:
            if row[0]:
                ret_list.append({'class_type': row[0], 'number': row[1]})
        return ret_list

    def get_category_content_data(self, category_type):
        print('sql_select_table category_type : ', category_type)
        sql_select_table = "SELECT remarks FROM `UserTable` WHERE class_type==%s" % ('"' + category_type + '"')
        print('sql_select_table : ', sql_select_table)
        cursor = self.db.execute(sql_select_table)
        ret_list = list()
        for row in cursor:
            ret_list.append({'remarks': row[0]})
        return ret_list

    def clear_all_data(self):
        try:
            empty_data = 'Delete FROM `UserTable`'
            self.db.execute(empty_data)
            self.db.commit()
        except BaseException as e:
            self.db.rollback()


if __name__ == '__main__':
    t_sqlite3 = SqlitePersist()
    t_sqlite3.connect()
    # t_sqlite3.insert_table_dict({'created': 'Test1', 'custom_id': 'XXXXXXXXXXXXX'})
    print('Sqlite3Persistence get Test2: ' + str(t_sqlite3.get_dict_by_custom_id('58ede5424c5c5000a8b47d82')))
    # print('Sqlite3Persistence get All: ' + str(t_sqlite3.get_dict_by_custom_id()))
    t_sqlite3.close()
