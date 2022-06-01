### Marketforce-interview

**Project Description**

_Python Version: 3.10_
_Type Checker: [Pyright](https://github.com/Microsoft/pyright)_

> The entry point of the project is the `main.py` file

There are two classes that inherit the base `Controller` class:

- `CSVController` - responsible for the interaction with the CSV file
- `SQliteController` - responsible for the interaction with the SQLite database

You can test the application by running the following command:

```
python main.py
```

> > _Unittests_

- The `unittest` module is used to test the application. You can run the tests by running the following command:

```
python -m unittest discover -v
```

> > _Type Checking_

- Run the following command to run the type checker:

```
pyright main.py
```
