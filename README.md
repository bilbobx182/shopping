## Grocery checker!
This project is a grocery store checker to scrape the websites to find the cheapest item in the stores.
Also useful to track price changes over time as we store things every 30 days.

## Backend

Python FAST API wrapped in a docker container. 
API endpoints will reach out to retailers, scrape, and insert data to the DB.

## Frontend

Angular v11.1.4 behind an Nginx reverse proxy in a docker container that talks to the backend.

## Infrastructure

- EC2 t2.micro instance to host backend and frontend.
- Security groups configured (443/8000) to allow traffic in and out of the VPC.
- RDS instance created to store data.

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
       url VARCHAR NOT NULL,
       other VARCHAR
   );
```

- A feature I would like to Add is have a historical_price where we just note a price and a product ID.

## Manual changes

- To generate the SSL certificates we used Certbot :
`sudo certbot certonly --manual --preferred-challenges=dns --email onuallainc@gmail.com --server https://acme-v02.api.letsencrypt.org/directory --agree-tos -d *.taifuwiddies.net`