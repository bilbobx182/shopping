## Grocery checker!
This project is a grocery store checker to scrape the websites to find the cheapest item in the stores.
Also useful to track price changes over time as we store things every 30 days.

![Demo gif of the functionality in V1!](https://i.imgur.com/MlELo8J.gif)


[Prototype demo and explanation on youtube](https://www.youtube.com/watch?v=R-QvetimMjE)

## Why you should care about this project

##### The buzzwords.
Let's just get them out of the way here : Docker,Angular,Nginx,FastAPI,Python,AWS,Postgres,SSL,Certbot.

This is the sales pitch about why this is cool, where the complexity is in the project.

- Good example of multi-stage docker images.
    - Good use of Nginx as a reverse proxy.
- Example of using FastAPI and Docker to perform web-scraping.
- Generating and using SSL certificates to make applications more secure.
- How networking works in the full-stack of an application lifecycle.
- Using ECR to manage docker images to build locally with a lot more ram rather than on a poor t2.micro.
- Using Postgres as a database solution with RDS.
####  Diagrams
### Simple Diagram
![Basic Diagram](https://i.imgur.com/HpOiY93.png)
#### Sequence Diagram
![Sequence Diagram](https://i.imgur.com/doP0B4Y.png)



## Backend

Python FAST API wrapped in a docker container. 
API endpoints will reach out to retailers, scrape, and insert data to the DB.

## Frontend

Angular v11.1.4 behind an Nginx reverse proxy in a docker container that talks to the backend.

## Infrastructure

- EC2 t2.micro instance to host backend and frontend.
- Security groups configured (443/8000) to allow traffic in and out of the VPC.
- RDS instance created to store data.
- Route53 for DNS
- Certbot / LetsEnrypt used for SSL.

#### RDS Table
```
 CREATE TABLE product (
       id serial PRIMARY KEY,
       catagory  VARCHAR NOT NULL,
       description VARCHAR  NOT NULL,
       retailer VARCHAR  NOT NULL,
       price FLOAT NOT NULL,
       last_updated TIMESTAMP NOT NULL ,
       brand VARCHAR NOT NULL,
       sku VARCHAR NOT NULL,
       url VARCHAR UNIQUE NOT NULL,
       other VARCHAR
   );


CREATE TABLE historical_prices ( 
 id serial PRIMARY KEY, 
 url VARCHAR NOT NULL, 
 price FLOAT NOT NULL, 
 last_time TIMESTAMP NOT NULL, 
 CONSTRAINT productIDCon FOREIGN KEY ( url ) REFERENCES public.product ( url ) 
); 
```

- A feature I would like to Add is have a historical_price where we just note a price and a product ID.

## Manual changes

- To generate the SSL certificates we used Certbot :
`sudo yum install -y https://dl.fedoraproject.org/pub/epel/epel-release-latest-7.noarch.rpm`
`sudo certbot certonly --manual --preferred-challenges=dns --email onuallainc@gmail.com --server https://acme-v02.api.letsencrypt.org/directory --agree-tos -d *.taifuwiddies.net`


## Things I'd like to do !

- [ ] Add image rendering to frontend.
- [ ] Add analytics tickers for what's going up and down in prices.
- [ ] Add historical changes to a given product view.
- [ ] Add metrics about what's most interesting.
