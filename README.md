# Data processing service and marketplace simulation
The project consists of 2 django projects:
- marketplace simulation, that supports methods for adding products, measure units and categories to backend Postgres, and requesting processing service for data upload
- processing service, that receives XML data via POST request from Enterprise Resource Planning system, converts it to JSON and sends to the marketplace endpoints by request

## How to start the API from Docker

1. `git clone https://github.com/mieltn/agora-hack.git -b develop`
2. `docker compose build` to build Docker images. You need to have Docker and Docker Compose installed.
3. `docker compose up` to start the marketplace (port 3000) and the processing service (port 2000). Both will be available on `http://0.0.0.0:{port}/`

## Functionality and testing

- To test both services first a POST request to `http://0.0.0.0:2000/uploadxml/` with XML body from <i>testing</i> should be sent. Data will be converted to JSON and stored in MongoDB on the processing server's side.
- To test getting data from processing service a GET request should be send to the marketplace `http://0.0.0.0:3000/upload/`. Marketplace will ask processing service to send preprocessed data.
- After receiving the feedback you can enter Postgres on the marketplace's side to inspect uploaded data with SQL.
- If you want to upload data once again it's better to clear MongoDB on the processing service's side and Postgres on the marketplace's side.
- If testbigdata.xml will be used, be prepared to wait around 5 minutes until all new items will be written to the marketplace's database.