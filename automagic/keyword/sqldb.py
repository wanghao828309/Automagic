# -*-coding:utf-8-*-s
# mysql和sqlserver的库
import pymysql
from DBUtils.PooledDB import PooledDB


class Database:
    def __init__(self, *db):
        if len(db) == 5:
            # mysql数据库
            self.host = db[0]
            self.port = int(db[1])
            self.user = db[2]
            self.pwd = db[3]
            self.db = db[4]
        self._CreatePool()

    def _CreatePool(self):
        if not self.db:
            raise NameError + "没有设置数据库信息"
        self.Pool = PooledDB(creator=pymysql, mincached=2, maxcached=5, maxshared=3, maxconnections=6, blocking=True,
                             host=self.host, port=self.port, \
                             user=self.user, password=self.pwd, database=self.db, charset="utf8")

    def _Getconnect(self):
        self.conn = self.Pool.connection()
        cur = self.conn.cursor()
        if not cur:
            raise ("数据库连接不上")
        else:
            return cur

    # 查询sql
    def execQuery(self, sql, count=0):
        cur = self._Getconnect()
        cur.execute(sql)
        if count == 1:
            res = cur.fetchone()
        else:
            res = cur.fetchall()
        cur.close()
        self.conn.close()
        return res

    # 非查询的sql
    def execNoQuery(self, sql):
        cur = self._Getconnect()
        cur.execute(sql)
        self.conn.commit()
        cur.close()
        self.conn.close()


if __name__ == '__main__':
    mydb = Database('10.10.19.117', 3306, 'root', 'root', 'filmora_es_admin')
    result = mydb.execQuery('SELECT catname from wx_resource_category where catdir="sound_electronic" ',1)
    result2 = mydb.execQuery('SELECT catname from wx_resource_category where catdir="sound_electronic" ')
    print result
    print result2
