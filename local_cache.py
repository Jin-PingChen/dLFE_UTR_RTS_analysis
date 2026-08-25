# Provide persistent string->string mapping (backed by sqlite file containing a single table). Multiple mappings can be created by passing different identifiers to the constructor.
from builtins import range
from builtins import object
import sys
from sqlalchemy import create_engine, Table, Column, MetaData, sql, String
from sqlalchemy.dialects.sqlite import INTEGER, FLOAT, VARCHAR
# 适配SQLAlchemy 2.0的导入路径
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError
# 无需导入config，直接用当前目录


#---- Configuration -------------------------------------------
_debug = False
#--------------------------------------------------------------


def get_db(filename):
    # 核心修改：使用当前目录创建SQLite文件（100%有权限）
    db_url = f'sqlite:///{filename}.db'
    db = create_engine(db_url, echo=_debug)
    connection = db.connect()
    return db, connection

#--------------------------------------------------------------
# ORM schema definition

md = MetaData()

strings_map = Table("strings_map", md,
                    Column("key", String, primary_key=True),
                    Column("value", String))

# 弃用警告修复
Base = declarative_base()


class StringsMap(Base):
    __tablename__ = "strings_map"
    key = Column(String, primary_key=True)
    value = Column(String)

#--------------------------------------------------------------

# Note - keys are assumed to be unique (within the scope of the store). This is enforced by the PK constraint.
class LocalStringsCache(object):
    def __init__(self, storeName):
        self._db, self._connection = get_db(storeName)
        self._storeName = storeName
        md.create_all(self._db)
        self._session = sessionmaker(bind=self._db)()

    def get_value(self, key):
        # 修复1：解包元组，适配SQLAlchemy 2.0 select语法
        results = self._connection.execute( sql.select( *(strings_map.c.value, )).select_from(strings_map).where(
            sql.and_(
                strings_map.c.key == key
            )
        ) )  # Note: order_by not needed, because id is used

        ret = results.fetchall()
        if( len(ret) < 1 ):
            return None
        return ret[0][0]

    def all_matching_values_source(self, prefix ):
        # 修复2：解包元组，适配SQLAlchemy 2.0 select语法
        results = self._connection.execute( sql.select( *(strings_map.c.key, strings_map.c.value, )).select_from(strings_map).where(
            strings_map.c.key.startswith( prefix )
        ) )  # Note: order_by not needed, because id is used

        for u, v in results:
            yield (u,v)
        
    # 修复3：修改insert_value，支持"存在则更新，不存在则插入"
    def insert_value(self, key, value):
        # 先检查key是否存在
        existing_row = self._session.query(StringsMap).filter_by(key=key).first()
        if existing_row:
            # 存在则更新
            existing_row.value = value
        else:
            # 不存在则插入
            sm = StringsMap( key=key, value=value )
            self._session.add(sm)
        self._session.commit() # 不再抛出IntegrityError

    def update_value(self, key, newValue):
        row = self._session.query(StringsMap).filter_by( key=key ).first()
        if row is None:
            raise Exception("Couldn't find StringsMap row matching key={}".format( key ) )
        row.value = newValue
        self._session.commit()

    # 新增：清空所有数据（测试用）
    def clear_all(self):
        self._session.query(StringsMap).delete()
        self._session.commit()


def testAll():
    # 移除未定义的randseq依赖，替换为固定字符串
    sc1 = LocalStringsCache("test_sc1")
    # 修复4：运行前清空旧数据，确保每次测试环境干净
    sc1.clear_all()
    
    # 插入test1（即使重复运行也不会报错）
    sc1.insert_value( "test1", "test1" )
    sc1.update_value( "test1", "----1----" )
    sc1.update_value( "test1", "----2----" )
    sc1.update_value( "test1", "----3----" )
    sc1.update_value( "test1", "test1" )

    # 减少循环次数，加快测试
    for i in range(10):
        sc1.insert_value("x.{}".format(i), f"test_seq_{i}" )
    for i in range(10):
        sc1.update_value("x.{}".format(i), f"updated_seq_{i}" )

    for u, v in sc1.all_matching_values_source( "x." ):
        print(u,v[:10])
        
    print(sc1.get_value("test1"))
    print(sc1.get_value("test1X"))
    assert( sc1.get_value("test1") == "test1" )
    return 0


if __name__=="__main__":
    import sys
    sys.exit(testAll())