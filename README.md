## **WatchTower**

### **Collect Error Logs from a number of applications**

To start with this repo, run the following command to build the repo
```bash
docker-compose -p watchtower build
```

Once the containers have been built, use the following commands to start up the container
```bash
docker-compose -p watchtower up -d
```

This starts the containers in `detach` mode.

### **How to use**
> Please Note, this  **_How to Use_** shows the steps for localhost

To send the error, it's advisable to use a background service to send the requests.
It works effectively in try..catch blocks, error handlers e.t.c

Data sample to send:
```json
{
  "clientIp": "IP Address of client that triggered the error",
  "service": "Unique name of the application/microservice where the error is triggered",
  "errorMessage": "A user readable form of the error message",
  "stackTrace": "The entire Exception in string form",
  "clientId": "Unique Identification for Client"
}
```

Send a POST request to `0.0.0.0:5000/save` with the above data sample

TODO:
- Authentication
- Token based request

