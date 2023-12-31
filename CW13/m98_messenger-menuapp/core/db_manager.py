from base import BaseManager, BaseModel
import psycopg2 as pg
import psycopg2.extras
from models import User, Message

class DBManager(BaseManager):
    
    def __init__(self, config: dict) -> None:
        super().__init__(config)  # {'db_config':{'dbname':'', 'host':'', 'password':'', 'user':'', ...}}
        self._db_config = config['db_config']
        self.__conn = pg.connect(**self._db_config)  # pg.connect(dbname='pg', host='localhost', ...)

    @staticmethod
    def converter_model_to_query(value):
        if isinstance(value, str):
            return f"'{value}'"
        elif value is None:
            return 'NULL'
        else:
            return str(value)

    
    def create_table(self, model_cls: type):
        assert issubclass(model_cls, BaseModel)

        with self.__conn.cursor() as curs:
            cols_dict = model_cls._get_columns()
            sql_cols = ','.join([" ".join(v) for v in cols_dict.values()])
            curs.execute(f"CREATE TABLE {model_cls.TABLE_NAME} ({sql_cols});", )
        
        self.__conn.commit()
    
    def _check_table_exists(self,  model_cls: type):
        with self.__conn.cursor() as curs:
            curs.execute("SELECT * FROM information_schema.tables WHERE table_name=%s",
                        (model_cls.TABLE_NAME,))
            return bool(curs.fetchone())
    
    def read_user_by_username(self, username: str) -> User:
        with self.__conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as curs:
            curs.execute(f"SELECT * FROM {User.TABLE_NAME} WHERE username = %s", (username,))
            user_data = curs.fetchone()
            if user_data:
                return User.from_dict(user_data)
            else:
                return None

    def get_inbox_messages(self, user_id: int):
        with self.__conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as curs:
            curs.execute(f"SELECT * FROM {Message.TABLE_NAME} WHERE to_user = %s", (user_id,))
            messages_data = curs.fetchall()
            return [Message.from_dict(data) for data in messages_data]

    def get_outbox_messages(self, user_id: int):
        with self.__conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as curs:
            curs.execute(f"SELECT * FROM {Message.TABLE_NAME} WHERE from_user = %s", (user_id,))
            messages_data = curs.fetchall()
            return [Message.from_dict(data) for data in messages_data]



    def create(self, m: BaseModel):
        if not self._check_table_exists(m.__class__):
            self.create_table(m.__class__)
        
        model_data = m.to_dict()  # {'_id':1, 'username':'akbar', ...}
        converter = self.converter_model_to_query

        with self.__conn.cursor() as curs:
            keys = ','.join(model_data.keys())
            values = ','.join(map(converter, model_data.values())) # 1, 'akbar', 'akbar1',... -> 1, 'akbar', 'akbar1' -> "1, 'akbar', 'akbar1'"
            curs.execute(f"INSERT INTO {m.TABLE_NAME} ({keys}) VALUES ({values}) RETURNING _id")
            new_model_id = curs.fetchone()[0]
            m._id = new_model_id
        
        # INSERT INTO users (_id, username, ...) VALUES (2, 'akbar', ...)
        self.__conn.commit()
        return new_model_id


    def read(self, id: int, model_cls: type) -> BaseModel:
        assert issubclass(model_cls, BaseModel)
        assert getattr(model_cls, 'TABLE_NAME', None), "Could not find TABLE NAME"

        # Read from DB
        with self.__conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as curs:
            # (3, 'asqar', '@asqar', ....)
            # {'_id': 3, ...}
            curs.execute(f"SELECT * FROM {model_cls.TABLE_NAME} WHERE _id = %s", (id, ))
            model_data:dict = curs.fetchone()
            assert model_data, "Not found"
            return model_cls.from_dict(model_data)



    def update(self, m: BaseModel) -> None:
        assert getattr(m, '_id', None)
        
        converter = self.converter_model_to_query

        fresh_data = m.to_dict() # {'_id':1, 'username':'akbar', ...}
        id = fresh_data.pop('_id') # id = _id, fresh_data = {'username':'akbar', ...}

        # dict..items() -> [('username', 'akbar'), (...)]
        # before join -> ["username='akbar'", "firstname='asqar'"]
        # after join -> "username='akbar', firstname='asqar', ..."
        updates = ','.join(map(lambda item: item[0]+'='+ f"{converter(item[1])}", fresh_data.items()))
        print("updates:", updates)
        
        with self.__conn.cursor() as cur:
            cur.execute(f"UPDATE {m.TABLE_NAME} SET {updates} WHERE _id = %s;", (id, ))
        
        self.__conn.commit()



    def delete(self, id: int, model_cls: type) -> None:
        assert getattr(model_cls, 'TABLE_NAME', None), "Could not find TABLE NAME"

        with self.__conn.cursor() as curs:
            curs.execute(f"DELETE FROM {model_cls.TABLE_NAME} WHERE _id = %s", (id, ))
        self.__conn.commit()



    def read_all(self, model_cls: type):
        assert issubclass(model_cls, BaseModel)
        assert getattr(model_cls, 'TABLE_NAME', None), "Could not find TABLE NAME"

        with self.__conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as curs:
            curs.execute(f"SELECT * FROM {model_cls.TABLE_NAME}")
            # Fetch list of dictionary
            models_data = curs.fetchall()
        
        # Convert to model instance
        for model_data in models_data:
            yield model_cls.from_dict(model_data)
        


    def truncate(self, model_cls: type) -> None:
        assert issubclass(model_cls, BaseModel)
        assert getattr(model_cls, 'TABLE_NAME', None), "Could not find TABLE NAME"

        with self.__conn.cursor() as curs:
            curs.execute(f"TRUNCATE TABLE {model_cls.TABLE_NAME}")
        self.__conn.commit()

    
    @property
    def connection(self):
        return self.__conn
