import copy
from poster.db.connection.connect import DbConnection


class QuerySet(DbConnection):
    def __init__(self, table_name, is_execute=True):
        self._get_query = "SELECT $Fields FROM $PrimeTable"
        self._create_query = """INSERT INTO table_name ($Fields)
                                VALUES ($Values); """
        self._update_query = """
            UPDATE $PrimeTable
            SET $KWARGS
        """
        self._query = None
        self._where = None
        self._fields = None
        self._single = False
        self.is_update_or_create = False
        self.table_name = table_name
        self._params = ()
        self._update_params = ()
        self._order_by = None
        self.is_execute = is_execute

    @classmethod
    def ready_for_set(cls, separating_str, kwargs, old_value=None):
        value = f"{old_value} {separating_str} " if old_value else ""
        value += f" {separating_str} ".join(
            [f"{element} = %s " for element in kwargs.keys()]
        )
        return value

    def fire_query(self, is_commit=False):
        query = self.set_final_query()
        query += f" where {self._where}"
        self._update_params += self._params
        result = self.db_execute(query, self._update_params, is_commit)
        _result = []
        if not self.is_update_or_create:
            _result = copy.deepcopy(result.fetchall())
            result.close()
        return _result

    def __iter__(self):
        if self.is_execute:
            self._params = {} if not self._params else self._params
            _result = self.fire_query()
            for element in _result:
                yield element

    def __getitem__(self, item):
        if isinstance(item, int):
            _result = self.fire_query()
            if len(_result) < abs(item):
                raise AttributeError(f"List out of index")
            return _result[item]

    def all(self):
        """To select all objects from the extended model without any filtration"""
        return self

    def filter(self, **kwargs):
        """To select filtered objects from the extended model without any filtration"""
        self._where = self.ready_for_set("and", kwargs, self._where)
        self._params += tuple(kwargs.values())
        return self

    def bulk_insert(self, rows: list):
        """To insert more than one object at same time inside database"""
        return self

    def update(self, **kwargs):
        """To update specific from the extended model"""
        self._query = self._update_query
        self._fields = self.ready_for_set(",", kwargs)
        self._update_params += tuple(kwargs.values())
        self.is_update_or_create = True
        return self.fire_query(is_commit=True)

    def create(self):
        pass

    def delete(self):
        """To delete specific from the extended model"""
        return self

    def values(self, *args):
        self._fields = args if len(args) else None
        return self

    def first(self):
        return self.__getitem__(0)

    def last(self):
        return self.__getitem__(-1)

    def set_final_query(self):

        if not self.is_update_or_create:
            self._fields = ["*"] if not self._fields else self._fields
            self._get_query = self._get_query.replace("$PrimeTable", self.table_name)
            self._get_query = self._get_query.replace("$Fields", ",".join(self._fields))
            return self._get_query
        if self._query:
            self._query = self._query.replace("$KWARGS", self._fields) if self._update_params else self._query
            self._query = self._query.replace("$PrimeTable", self.table_name)
            return self._query
        raise AttributeError("No Query Set")
