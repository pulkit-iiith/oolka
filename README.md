# YouTube Video Fetch API

This FastAPI application serves as an Event Manager API that allows users to manage events and book tickets for these events.
The application is structured with separate endpoints for handling events and bookings.
The database operations are managed using SQLAlchemy,and the application includes necessary setups to initialize the database and create tables.


## Setup Instructions

### Prerequisites:
1. Python 3.x
2. MySQL Server
3. Fast API


### Installation
To run the server and test the API locally, follow these steps:
  1. Clone the repository:
     ```
     git clone https://github.com/pulkit-iiith/oolka.git
      ```
  2. Build and start docker server:

     First start docker doemon
     ```
     docker-compose up -d
     ```
    
Once the containers are up and running, you can access the API endpoints.

## API Endpoints:

  1. Add Events
      - Endpoint: /events
      - Method: POST
  2. Get Event with id
      - Endpoint: /events/{id}
      - Method: GET
  3. Get All Events
      - Endpoint: /events/
      - Method: GET
  4. Book events
      - Endpoint: /bookings/{id}/book
      - Method: Post
  
    
  For json parameter details you can start docker and go to link http://localhost:5001/docs for swagger as I have hosted docker on port 5001
   
## Testing the API :

  You can test the API endpoints using tools like cURL or Postman. Here are some examples:

      1. Add events
      
      curl http://localhost:5001/events

      Example Json:- {
    "name": "water Concert",
    "date": "2023-12-31",
    "location": "Madison Square Garden",
    "total_tickets": 5000,
    "event_type":"music festival"
}

      
      2. get event with id
      
      curl http://127.0.0.1:5001/events/1
      
      3. get events
      
      curl http://127.0.0.1:5001/events
      
      4. book events
      
      curl http://127.0.0.1:5001/bookings/1/book

      Example Json:- {
    "tickets":600
}
      

## Giving parameters in docker-compose.yml:

We have a docker-compose.yml file which contains all the environments variables which looks like:-
```
version: '3'

services:
  app:
    build: .
    ports:
     - "5001:8000"
    volumes:
     - .:/app
    depends_on:
      - mysql
    environment:
      - MYSQL_HOST=mysql
      - MYSQL_USER=root
      - MYSQL_PASSWORD=admin 
      - MYSQL_DB=test

  mysql:
    image: mysql:latest
    environment:
      - MYSQL_HOST=mysql
      - MYSQL_PASSWORD=admin
      - MYSQL_DB=test
      - MYSQL_ROOT_PASSWORD=admin

    ports:
      - "3306:3306"

```
## Test cases:

Run command pytest

## Swagger

After running command:- docker-compose up -d  Swagger will start on :- http://localhost:5001/docs

## Explanation

After this submission I will create a video explaining all the details that I have implemented.


      
  
