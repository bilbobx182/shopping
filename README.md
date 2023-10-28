## Grocery checker!
This project was originally a project to get the cost of groceries by scraping sites and then rendering it on a lovely UI.

![Demo gif of the functionality in V1!](https://i.imgur.com/MlELo8J.gif)
[Prototype demo and explanation on youtube](https://www.youtube.com/watch?v=R-QvetimMjE)

Since then, I've removed my AWS infrastructure, but I've kept the project alive.
Right now I use it to render a CSV file to the terminal so that I can see which store is overall better.
An example is this [google sheets page here](https://docs.google.com/spreadsheets/d/1nlqonXP0vKKTPQcIkuet2zFRE1RKPH6yNlCOKZy5a-c/edit?usp=sharing)

##### The buzzwords.
Docker ,Angular, Nginx, FastAPI, Python, AWS, Postgres, SSL, Certbot.

## Why you should care about this project
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
ALTER TABLE historical_prices ADD UNIQUE(url); 
```

- A feature I would like to Add is have a historical_price where we just note a price and a product ID.

## Manual changes

- To generate the SSL certificates we used Certbot :
`sudo yum install -y https://dl.fedoraproject.org/pub/epel/epel-release-latest-7.noarch.rpm`
`sudo certbot certonly --manual --preferred-challenges=dns --email onuallainc@gmail.com --server https://acme-v02.api.letsencrypt.org/directory --agree-tos -d *.taifuwiddies.net`

## Feedback I actioned on so far V1.

- [x] Storing historical prices and updating current products.
- [x] Fixed scrolling on many results returned.
- [x] Overall website theme to be less dark.
- [x] Added last updated field to the UI.
- [x] URL colour changed.
- [x] Fixed the CSS.
- [x] Added rendering of a CSV to see prices.

## Things I'd like to do !

- [ ] Weekly price seeding.
- [ ] Add image rendering to frontend.
- [ ] Add analytics tickers for what's going up and down in prices.
- [ ] Add historical changes to a given product view.
- [ ] Add metrics about what's most interesting.

### How do I run it?
As it stands right now I have it configured to render data to terminal.
_note sometimes on macs docker networking may not be able to connect to the internet and this will do nothing_.
`docker build -t grocer_back -f backend.Dockerfile .`
`docker run grocer_back`
`./bin/build.sh`
