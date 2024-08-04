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
1. Verify if you have Python version newer than 3.9.
2. Install requirements.txt (preferably into virtual environment).
3. Go to main project folder at */main* and run ```python manage.py migrate``` to  create database and migrate models.
4. Optionally create an API key:
   1. Open project shell ```python manage.py shell```
   2. Import ApiKeys model ```from api.models import ApiKeys```
   3. Add new key ```key = ApiKeys(api_key=[api_key], valid_to=[date])```
   4. Save new key ```key.save()```
5. Run server using ```python manage.py runserver```
6. Access the api at ```localhost:8000/api/validate``` or using provided **validate_api.ipynb** script.