# Diet2020

Domain name: http://tastytarget.com/

Data source: https://www.allrecipes.com/ and USDA

## Backend
### graphql-python
Tutorial: https://github.com/howtographql/graphql-python

GraphiQL: http://localhost:8000/graphql/

Instructions:

- Run the server:
```python
source activate graphql
cd graphql-python
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```
- Create a query:
```
query {
  links {
    id
    description
    url
  }
}
```
