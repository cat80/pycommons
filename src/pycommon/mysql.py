import pymysql
import datetime


##
# <p>Copyright (c) 2016-2017 cat80 </p>
# <p>该文件是对mysql操作的封装</p>
# <p>封装的方法点多，具体再写吧</p>
# </br></br>
# <p>该文件引用了pymysql进行数据方法 </p>
##
class mysql:
    """
        mysql  辅助类
    """
    conn = None
    table = ''
    op = None
    datas = []
    condition = []
    current_sql = ''

    def __init__(self, connargs={}):
        config = {'host': 'localhost', 'user': 'root', 'passwd': '123456', 'port': 3306, 'charset': 'utf8',
                  'db': 'mysql'}
        for item in connargs:
            config[item] = connargs[item]
        self.conn = pymysql.connect(host=config['host'], user=config['user'], passwd=config['passwd'], db=config['db'],
                                    port=config['port'], charset=config['charset'])

    def close(self):
        self.conn.close()

    def query(self, sql, args=None):
        """
        根据sql语句进行查询
        :param sql:
        :param args:support tunlp ,dic...if the tunlp please use %(var)s repalce hold
        :return:
        """
        cur = self.conn.cursor(pymysql.cursors.DictCursor)
        cur.execute(sql, args)
        data = cur.fetchall()
        cur.close()
        return data

    def single(self, sql, args=None):
        """
        获取首行首列
        :param sql:
        :return:
        """
        data = self.query(sql, args)
        if data != None and len(data) > 0:
            for index in data:
                for item in index:
                    return index[item]
        return None

    def row(self, sql, args=None):
        """
        获取一行
        :param sql:
        :param args:
        :return:
        """
        data = self.query(sql, args)
        if data != None and len(data) > 0:
            return data[0];
        return None

    def execute(self, sql, args=None):
        """
        执行语句并且返回影响行数
        :param sql:
        :param args:
        :return:
        """
        cur = self.conn.cursor()
        effect_row = cur.execute(sql, args)
        self.conn.commit()
        cur.close()
        return effect_row

    def table(self, tablename):
        self.table = tablename
        return self

    def data(self, data):
        self.datas = data
        return self

    def current_date_time(self):
        return "{0:%Y-%m-%d %H:%M:%S}".format(datetime.datetime.now())

    def where(self, condition):
        self.condition = condition
        return self

    def add(self):
        """
        新增操作，一般是obj->table('table')->data([...])->add()的方法进行新增
        :return: 返回受影响行数
        """
        #     拼接SQL
        # insert into () values () ....
        self.current_sql = "insert into {2} ({0}) values ({1})".format(
            ','.join(['`{0}`'.format(item) for item in self.datas]),
            ','.join(['%({0})s'.format(item) for item in self.datas]),
            self.table
        )

        return self.execute(self.current_sql, self.datas)

    def update(self):
        """
        更新操作，一般写法为self.table('tab')->data({'uid':''})->where()->update()
        :return:
        """
        # `id` = 'id'
        self.current_sql = "UPDATE {0} SET {1}  WHERE ".format(self.table,
                                                               ",".join([" `{0}` = %({0})s ".format(item) for item in
                                                                         self.datas]))
        self.current_sql += self.where_str()
        # sql 写法 update tablename set where '' = %(where_)s
        return self.execute(self.current_sql, self.datas)

    def where_str(self):
        if isinstance(self.condition, str):
            return self.condition
        if isinstance(self.condition, dict):
            wherestr = ' and '.join([' {0} = %(where_{0})s  '.format(item) for item in self.condition])
            for item in self.condition:
                self.datas["where_" + item] = self.condition[item]
            return wherestr

    def close(self):
        if self.conn is not None:
            self.conn.close()


