# Diet2020

Domain name: http://tastytarget.com/

Data source: https://www.allrecipes.com/ and USDA

## Backend
### graphql-python
Tutorial: https://github.com/howtographql/graphql-python

GraphiQL: http://localhost:8000/graphql/

#### Instructions

Running the Server:
```
>>> source activate graphql
>>> cd graphql-python
>>> pip install -r requirements.txt
>>> cd hackernews
>>> python manage.py migrate
>>> python manage.py runserver
```
Creating a Query:
```
>>> python manage.py shell
>>> from links.models import Link
>>> Link.objects.create(url='https://www.howtographql.com/', description='The Fullstack Tutorial for GraphQL')
>>> Link.objects.create(url='https://twitter.com/jonatasbaldin/', description='The Jonatas Baldin Twitter')
```
```
query {
  links {
    id
    description
    url
  }
}
```
Creating a User:
```
mutation{
  createUser(username:"zeyu",
  email:"zeyuyang8@gmail.com",
  password:"diet2020"){
    user{
      id
      username
      email
    }
  }
}
```
Querying the Users:
```
query{
  users{
    id
    username
    email
  }
}
```
Configuring django-graphql-jwt:
```
mutation {
	tokenAuth(username:"zeyu",
  password:"diet2020"){
    token
  }
}
```
```
mutation {
	verifyToken(token:"eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VybmFtZSI6InpleXUiLCJleHAiOjE2MDM4ODcwNzQsIm9yaWdJYXQiOjE2MDM4ODY3NzR9.1kHiPFUPrZgcyY7EtqJLMXLIuZu3MP8l73C_iVlWn1g"){
    payload
  }
}
```
Attaching Users to Links:
```
mutation {
	createLink(
    url:"www.baidu.com",
    description: "great website"
  ){
    id
    url
    description
    postedBy{
      id
      username
      email
    }
  }
}
```
Adding Votes:
```
mutation {
	createVote(linkId:1){
    user {
      id
      username
      email
    }
    link {
      id
      description
      url
    }
  }  
}
```
Relating Links and Votes:
```
query{
  votes{
    id
    user{
      id
      username
    }
    link{
      id
      url
    }
  }
}
```
```
query{
  links{
    id
    url
    votes{
      id
      user {
        id
        username
      }
    }
  }
}
```
Filtering Links:
```
query{
	links(search:"jonatas"){
    id
    url
    description
  }
}
```
Paginating Links:
```
query{
	links(first:1,skip:1){
    id
    url
    description
  }
}
```
Using Relay on Links:
```
query{
	relayLinks(first:1){
    edges{
      node{
        id
        url
        description
      }
    }
    pageInfo{
      startCursor
      endCursor
    }
  }
}
```
Relay and Mutations:
```
mutation{
  relayCreateLink(input:{
    url: "tastytarget.com",
    description: "diet optimizer"
  })
  {
    link{
      id
      url
      description
    }
  }
}
```





