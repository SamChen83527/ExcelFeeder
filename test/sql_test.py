from sqlalchemy import create_engine, Table, Column, Integer, String, MetaData, ForeignKey, UniqueConstraint, Index
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy_utils import database_exists, create_database
from table_schema import AWANSHI_TABLE_SCHEMA


class DbContext():
    Base = declarative_base()

    def __init__(self, conn_str) -> None:
        self.connection_str = conn_str
        self.engine = self.__connect_db(conn_str)
        self.init_db()

    def __connect_db(self, conn_str: str):
        engine = create_engine(conn_str, echo=True)
        if not database_exists(engine.url):
            create_database(engine.url)

        print('Database connecting successfully: {}'.format(engine.url))
        return engine

    def init_db(self):
        __class__.Base.metadata.create_all(self.engine)

    def create_table(self):
        metadata = MetaData(self.engine)

        user = Table('user', metadata,
                     Column('id', Integer, primary_key=True),
                     Column('name', String(20)),
                     Column('fullname', String(40))
                     )
        address_table = Table('address', metadata,
                              Column('id', Integer, primary_key=True),
                              Column('user_id', None, ForeignKey('user.id')),
                              Column('email', String(128), nullable=False)
                              )

        metadata.create_all()

    def create_data_test(self):
        Session = sessionmaker(bind=self.engine)
        session = Session()

        obj = self.Users(name='Sam', extra='Chen')
        session.add(obj)
        # add_all 列表形式
        session.add_all([
            self.Users(name='Chloe', extra='Wu'),
            self.Users(name='Mary', extra='Lin')
        ])
        # 提交
        session.commit()

    class Users(Base):
        __tablename__ = 'users'
        id = Column(Integer, primary_key=True)
        name = Column(String(32))
        extra = Column(String(16))

        # __table_args__ = (
        #     UniqueConstraint('id', 'name', name='uix_id_name'),
        #     Index('ix_id_name', 'name', 'extra'),
        # )


if __name__ == '__main__':
    conn_str = "mysql+pymysql://root:88888888@localhost:3306/awanshi_db"
    db_ctx = DbContext(conn_str)
    db_ctx.create_data_test()
