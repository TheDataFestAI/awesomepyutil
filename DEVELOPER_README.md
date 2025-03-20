# How To Run Package From Local Machine (Windows)
    1. Clone the code from Github:
        ```shell
        git clone https://github.com/TheDataFestAI/awesomepyutil.git
        ```
	1. Create & activate Python Virtual Environment -
		```shell
		python -m venv .venv
		.\.venv\Scripts\activate
		```
	2. Install the python dependency packages -
		```shell
		python -m pip install --upgrade pip
		pip install setuptools>=75.0.0 build==1.2.2 twine==5.1.1
		pip install -r .\requirements.txt
		```
3. Build the package -
    ```shell
    py -m build
    py -m twine upload --repository testpypi dist/*
    py -m twine upload --repository pypi dist/*
    ```

4. test from local machine:
    ```shell
    # python setup.py sdist
    pip uninstall awesomepyutil
    pip install dist/awesomepyutil-0.0.2.tar.gz
    ```
4. Test from testpypi distribution:
    ```shell
    pip install --index-url https://test.pypi.org/simple/ --no-deps basicpkg
    ```
4. Run the testcase -
    ```shell
    py .\tests\test_arithmetic_operations.py
    # or
    py -m unittest tests.test_arithmetic_operations.TestArithmeticOperations
    ```

# Extras:

1. Extra Git Commands -
    ```shell
    git init -b main
    git add .
    git status
    git commit -m "First commit"
    git pull origin main --allow-unrelated-histories
    git branch -d dev
    git push -d origin dev


    git remote add origin https://github.com/TheDataFestAI/awesomepyutil.git
    git remote set-url origin https://<user_name>:<access_token>@github.com/TheDataFestAI/<repo_name>.git
    ```
# Reference:

1. Python PyPi Package -
    1. [ ] https://www.freecodecamp.org/news/how-to-create-and-upload-your-first-python-package-to-pypi/
    2. https://betterscientificsoftware.github.io/python-for-hpc/tutorials/python-pypi-packaging/

