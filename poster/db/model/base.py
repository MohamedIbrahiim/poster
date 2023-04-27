"""
This File will Hold all necessary function to create models
all () || filter () || update () || delete () || bulk update () || bulk create ()
"""
from poster.db.connection.query import QuerySet


# ------------ Manager (Model objects handler) ------------ #
class BaseManager(QuerySet):
    """
    class will hold all main functions for models
    """

    query = ""
    params = {}

    def __init__(self, model_class) -> None:
        """constractor implementation to add extended model class () inheritance"""
        self.model_class = model_class
        self.table_name = (
            self.model_class.table_name
            if self.model_class.table_name
            else self.model_class.__name__
        )
        super().__init__(self.table_name)

    def data(self):
        result = self.db_execute(self.query, tuple(self.params.values()))
        result.fetchall()
        # Execute query

        # Fetch data obtained with the previous query execution
        # and transform it into `model_class` objects.
        # The fetching is done by batches of `chunk_size` to
        # avoid to run out of memory.


# ----------------------- Model ----------------------- #
class MetaModel(type):
    """
    class will have manager class from base Manager, so we can call instance from BaseManager
    using .objects.
    """

    manager_class = BaseManager

    def _get_manager(cls) -> BaseManager:
        """create instance from Base manager to extend all methods"""
        return cls.manager_class(model_class=cls)

    @property
    def objects(cls) -> _get_manager:
        """return single object of function get from _get_manger"""
        return cls._get_manager()


class Model(metaclass=MetaModel):
    """
    class will hold every standard details for the model like model name
    """

    table_name = ""
