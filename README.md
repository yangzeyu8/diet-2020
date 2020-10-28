# Diet2020

Domain name: http://tastytarget.com/

Data source: https://www.allrecipes.com/ and USDA

## Backend
### graphql-python
Tutorial: https://github.com/howtographql/graphql-python

GraphiQL: http://localhost:8000/graphql/

Instructions:

- Running the Server:
```
source activate graphql
cd graphql-python
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```
- Creating a Query:
```
query {
  links {
    id
    description
    url
  }
}
```
- Creating a Link:
```
mutation {
  createLink(
    url: "https://github.com",
    description: "Lots of Code!"
    url
   ){
    id
    url
    description
    }
}
```
- Creating a Link:
```
mutation {
  createLink(
    url: "https://github.com",
    description: "Lots of Code!"
    url
   ){
    id
    url
    description
    }
}
```
- Creating a User:
```
mutation {
  createUser (
    username: "Zeyu",
    email: "zeyuyang8@gmail.com",
    password: "123"
    )
  user { 
    id
    username
    email
    }
}
```
- Querying the Users:
```
query {
  users {
    id
    username
    email
  }
}
```
- Configuring django-graphql-jwt:
```
mutation {
  tokenAuth (
    username: "Zeyu",
    password: "123"
    ){ 
    token
    }
}
```

```
mutation {
  verifyToken (
    token: "fjladkshflkgkasj"
    ){ 
    payload
    }
}
```

```
query {
  me {
    id
    username
  }
}
```





