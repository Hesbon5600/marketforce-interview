from abc import ABCMeta, abstractmethod
from collections import namedtuple
from dataclasses import asdict, dataclass
from typing import Any, Dict, List, Optional, Union
import csv
import sqlite3

from sql_queries import CREATE_TABLE_CAR, CREATE_TABLE_USER, INSERT_CAR, INSERT_USER


Car = namedtuple("Car", ["id", "color", "type", "model"])


@dataclass
class User:
    id: int
    name: str
    age: int

    def _asdict(self):
        return asdict(self)


@dataclass
class Controller(metaclass=ABCMeta):
    OBJ_MAPPER = {"user": User, "car": Car}

    @abstractmethod
    def create(self, data: Union[User, Car]) -> None:
        """
        Create a new object in the database or CSV file.
        To be implemented by subclasses.
        """
        ...

    @abstractmethod
    def get(self, obj_id: int, obj_type: str) -> Union[User, Car]:
        """
        Get an object from the database or CSV file.
        """
        ...

    def validate_base_objs(self, data: Union[User, Car]) -> None:
        """
        Validate the data object.
        Args:
            data: The data object to be validated.
        Raise:
            ValueError: If the data object is not an instance of User or Car.
        Returns:
            None
        """
        if not isinstance(data, User) and not isinstance(data, Car):
            raise TypeError(
                f"Invalid data type. Expected 'User' or 'Car' but got '{data.__class__.__name__}'"
            )

    def validate_obj_type(self, obj_type: str) -> None:
        """
        Validate the object type.
        Args:
            obj_type: The object type to be validated.
        Raise:
            ValueError: If the object type is not 'user' or 'car'.
        """
        if obj_type not in self.OBJ_MAPPER.keys():
            raise ValueError(
                f"Invalid obj_type. Expected 'user' or 'car' but got '{obj_type}'"
            )


class CSVController(Controller):

    CSV_MAPPER = {"user": "users.csv", "car": "cars.csv"}

    def create(self, data: Union[User, Car]) -> None:
        """
        Create a new object in the CSV file.
        Args:
            data: The data object to be created.
        Returns:
            None
        """
        self.validate_base_objs(data)
        dict_data = data._asdict()
        file_name = self.CSV_MAPPER.get(data.__class__.__name__.lower(), "")
        csv_data = self._get_csv_data(file_name)
        item_found = None
        if not csv_data:
            csv_data.append(dict_data)
        else:
            for item in csv_data:
                if item and (int(item["id"]) == dict_data["id"]):
                    item_found = item
                    break
            if not item_found:
                csv_data.append(dict_data)
            else:
                item_found.update(dict_data)
        self._write_data_to_csv(file_name, csv_data)

    def get(self, obj_id: int, obj_type: str) -> Union[User, Car]:
        """
        Get an object from the CSV file.
        Args:
            obj_id: The object id to be retrieved.
            obj_type: The object type to be retrieved.
        Raises:
            ValueError: If the object type is not found.
        Returns:
            The object retrieved.
        """
        self.validate_obj_type(obj_type)
        file_name = self.CSV_MAPPER.get(obj_type.lower(), "")
        data = self._get_csv_data(file_name)
        obj = User if obj_type.lower() == "user" else Car
        for item in data:
            try:
                if item and (int(item["id"]) == obj_id):
                    return obj(**item)
            except ValueError:
                pass
        raise ValueError(f"{file_name.title()} with id '{obj_id}' not found")

    @staticmethod
    def _get_csv_data(file_name: str) -> List[Optional[Dict[Any, Any]]]:
        """
        Get all the data from the CSV file.
        Args:
            file_name: The CSV file name.
        Returns:
            The data retrieved.
        """
        try:
            with open(file_name, "r") as csv_file:
                csv_reader = csv.DictReader(csv_file)
                return list(csv_reader)
        except FileNotFoundError:
            return []

    def _write_data_to_csv(self, file_name: str, data: List[Dict[Any, Any]]) -> None:
        """
        Write the data to the CSV file.
        Args:
            file_name: The CSV file name.
            data: The data to be written.
        Returns:
            None
        """
        with open(file_name, "w") as csv_file:
            csv_writer = csv.DictWriter(csv_file, fieldnames=data[0].keys())
            csv_writer.writeheader()
            csv_writer.writerows(data)


class SQliteController(Controller):
    def create(self, data: Union[User, Car]) -> None:
        """
        Create a new object in the database.
        Args:
            data: The data object to be created.
        Returns:
            None
        """
        self.validate_base_objs(data)
        table_name = data.__class__.__name__.lower()
        self._insert_data_to_table(table_name, data._asdict())

    def get(self, obj_id: int, obj_type: str) -> Union[User, Car]:
        """
        Get an object from the database.
        Args:
            obj_id: The object id to be retrieved.
            obj_type: The object type to be retrieved.
        Returns:
            The object retrieved.
        """
        self.validate_obj_type(obj_type)
        table_name = obj_type.lower()
        data = self._get_object_by_id(table_name, obj_id)
        if table_name == "user":
            return User(**data)
        return Car(**data)

    def _db_connection(self) -> sqlite3.Connection:
        """
        Get the database connection.
        Returns:
            The database connection.
        """
        return sqlite3.connect("test.db")

    def _execute_create_sql_query(self, query: str) -> None:
        """
        Execute the SQL query.
        Args:
            query: The SQL query to be executed.
        Returns:
            None
        """
        connection = self._db_connection()
        connection.execute(query)
        connection.commit()

    def _create_table_if_not_exists(self, table_name: str) -> None:
        """
        Create the table if it does not exist.
        Args:
            table_name: The table name.
        Returns:
            None
        """
        QUERY_MAPPER = {"user": CREATE_TABLE_USER, "car": CREATE_TABLE_CAR}

        query = QUERY_MAPPER.get(table_name, "")
        self._execute_create_sql_query(query)

    def _insert_data_to_table(self, table_name: str, data: Dict[Any, Any]) -> None:
        """
        Insert the data to the table.
        Args:
            table_name: The table name.
            data: The data to be inserted.
        Returns:
            None
        """
        if table_name == "user":
            query = INSERT_USER.format(
                id=data["id"], name=data["name"], age=data["age"]
            )
        else:
            query = INSERT_CAR.format(
                id=data["id"],
                color=data["color"],
                type=data["type"],
                model=data["model"],
            )
        self._create_table_if_not_exists(table_name)
        self._execute_create_sql_query(query)

    def _get_object_by_id(self, table_name: str, obj_id: int) -> Dict[Any, Any]:
        """
        Get the object by id.
        Args:
            table_name: The table name.
            obj_id: The object id.
        Raise:
            ValueError: If the object is not found.
        Returns:
            The object retrieved.
        """
        self._create_table_if_not_exists(table_name)
        query = f"SELECT * FROM {table_name} WHERE id={obj_id}"
        connection = self._db_connection()
        cursor = connection.execute(query)
        result = cursor.fetchone()
        if result:
            data = {}
            for idx, col in enumerate(cursor.description):
                data[col[0]] = result[idx]

            return data
        raise ValueError(f"{table_name.title()} with id '{obj_id}' not found")


if __name__ == "__main__":

    car = Car(id=4, color="blue", type="toyota", model="corolla")
    user = User(id=2, name="Bob", age=40)
    user_2 = User(id=2, name="Alice", age=30)

    sqlite_controller = SQliteController()

    sqlite_controller.create(user)
    # sqlite_controller.create(user_2)
    sqlite_controller.create(car)

    print("SQLite Controller\n\n")
    print("User -->", sqlite_controller.get(2, "user"))
    print("Car -->", sqlite_controller.get(4, "car"), "\n")
    print("\n")

    csv_controller = CSVController()

    csv_controller.create(user)
    csv_controller.create(user_2)
    csv_controller.create(car)

    print("CSV Controller\n\n")
    print("User -->", csv_controller.get(2, "user"))
    print("Car -->", csv_controller.get(4, "car"), "\n")
