# How To Run Package From Local Machine

1. Create & activate Python Virtual Environment -
    ```shell
    python -m virtualenv .venv
    .\.venv\Scripts\activate
    ```
2. Install the python dependent packages -
    ```shell
    python -m pip install --upgrade pip
    pip install -r .\requirements.txt
    ```
3. Build the package -
    ```shell
    py -m build
    py -m twine upload --repository testpypi dist/*
    py -m twine upload --repository pypi dist/*
    ```
4. Run the testcase -
    ```shell
    py .\tests\test_arithmetic_operations.py
    # or
    py -m unittest tests.test_arithmetic_operations.TestArithmeticOperations
    ```

# Reference:

1. Python PyPi Package -
    1. [ ] https://www.freecodecamp.org/news/how-to-create-and-upload-your-first-python-package-to-pypi/
    2. https://betterscientificsoftware.github.io/python-for-hpc/tutorials/python-pypi-packaging/

