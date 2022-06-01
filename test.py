import unittest

from main import CSVController, SQliteController, User, Car


class BaseTest(unittest.TestCase):
    """
    CSV test cases
    """

    def setUp(self):
        self.users = [
            User(1, 'John', 20),
            User(2, 'Mary', 30),
            User(3, 'Mike', 40)
        ]
        self.cars = [
            Car(1, 'red', 'toyota', 'corolla'),
            Car(2, 'blue', 'toyota', 'camry'),
            Car(3, 'green', 'ford', 'mustang')
        ]


class TestCSVController(BaseTest):
    """
    CSV Controller test cases
    """

    def setUp(self):
        super(self.__class__, self).setUp()
        self.csv_controller = CSVController()
        self.initial_data()

    def initial_data(self):
        """
        Initial data
        """
        for user in self.users:
            self.csv_controller.create(user)

        for car in self.cars:
            self.csv_controller.create(car)

    def test_add_to_csv_succeeds(self):
        """
        Test add to csv successfully
        """
        user = self.users[0]
        car = self.cars[0]

        self.csv_controller.create(user)
        self.csv_controller.create(car)
        saved_user = self.csv_controller.get(user.id, 'user')
        saved_car = self.csv_controller.get(car.id, 'car')

        self.assertEqual(user.id, int(saved_user.id))
        self.assertEqual(user.name, saved_user.name)
        self.assertEqual(car.id, int(saved_car.id))
        self.assertEqual(car.color, saved_car.color)

    def test_add_to_csv_fails(self):
        """
        Test add to csv fails
        """
        invalid_user_type = {'id': 1, 'name': 'John', 'age': 20}
        invalid_car_type = {'id': 1, 'color': 'red',
                            'type': 'toyota', 'model': 'corolla'}
        with self.assertRaises(TypeError):
            self.csv_controller.create(invalid_user_type)
        with self.assertRaises(TypeError):
            self.csv_controller.create(invalid_car_type)

    def test_get_from_csv_fails(self):
        """
        Test get from csv fails
        """
        with self.assertRaises(ValueError):
            self.csv_controller.get(100, 'user')
        with self.assertRaises(ValueError):
            self.csv_controller.get(100, 'car')


class TestSQliteController(BaseTest):
    """
    SQlite Controller test cases
    """

    def setUp(self):
        super(self.__class__, self).setUp()
        self.sqlite_controller = SQliteController()
        self.initial_data()

    def initial_data(self):
        """
        Initial data
        """
        for user in self.users:
            self.sqlite_controller.create(user)

        for car in self.cars:
            self.sqlite_controller.create(car)

    def test_add_to_sqlite_succeeds(self):
        """
        Test add to sqlite successfully
        """
        user = self.users[0]
        car = self.cars[0]

        self.sqlite_controller.create(user)
        self.sqlite_controller.create(car)
        saved_user = self.sqlite_controller.get(user.id, 'user')
        saved_car = self.sqlite_controller.get(car.id, 'car')

        self.assertEqual(user.id, int(saved_user.id))
        self.assertEqual(user.name, saved_user.name)
        self.assertEqual(car.id, int(saved_car.id))
        self.assertEqual(car.color, saved_car.color)

    def test_add_to_sqlite_fails(self):
        """
        Test add to sqlite fails
        """
        invalid_user_type = {'id': 1, 'name': 'John', 'age': 20}
        invalid_car_type = {'id': 1, 'color': 'red',
                            'type': 'toyota', 'model': 'corolla'}
        with self.assertRaises(TypeError):
            self.sqlite_controller.create(invalid_user_type)
        with self.assertRaises(TypeError):
            self.sqlite_controller.create(invalid_car_type)

    def test_get_from_sqlite_fails(self):
        """
        Test get from sqlite fails
        """
        with self.assertRaises(ValueError):
            self.sqlite_controller.get(100, 'user')
        with self.assertRaises(ValueError):
            self.sqlite_controller.get(100, 'car')
