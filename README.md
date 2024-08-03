# Django API 
## Description
This API is designed to validate input data to match set schema. Then as response it returns amount of valid and invalid values in the list. Input data should be list of dictionaries where each dictionary has a number as a key and text as value (```[{num:text}]```) , so for example:
```
[
    {1:'foo'},
    {'foo':'bar'},
]
```
the result will be like:
```
{
    'valid':    1,
    'invalid':  1,
}
```
## Installation
1. Verify if you have Python version newer than 3.9
2. Install requirements.txt (preferably into virtual environment)
3. Go to main project folder at main/main and run ```python manage.py migrate```
4. Run server using ```python manage.py runserver```
5. Access the api at ```localhost:8000/api/validate```