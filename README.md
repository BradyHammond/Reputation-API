# Overview
The reputation API is a simple API implemented using Python 3.6 and the Falcon API framework. It has a single endpoint that can take either a POST or a GET method. Data sent in a POST to the API, simply gets stored in a database. Upon a GET request, data is pulled from the database, processed, and returned to the requester. Reputation data includes clarity, clout, and reach statistics.
# Setup
To setup the API on your own computer you will first need [Python 3.6](https://www.python.org/downloads/). Once, this is downloaded you will also need virtualenv which is a Python module that let's you setup your own virtual environment. With your download of Python 3.6, there should have been a command-line tool installed on your computer called pip3. To check if pip3 was successfully installed on your machine, open a terminal (or command prompt if you're on Windows), and run one of the following commands: `pip3 -V` or `pip3 --version`. If you recieve an error message similar to this one: `bash: pip: command not found`, run the command `sudo easy_install3 pip` (on Debian/Ubuntu distros of Linux, you may first have to run the command `sudo apt-get install python3-setuptools` before easy_install3 is available). For more information on downloading and installing pip3 visit [https://pip.pypa.io/en/stable/installing/](https://pip.pypa.io/en/stable/installing/). With Python 3.6 and pip3 both installed, you can now install [virtualenv](https://virtualenv.pypa.io/en/stable/) by running the command `pip3 install virtualenv` from the command-line.

With all the prerequisites downloaded and installed, you can now run the following commands to setup the API in a virtual environment:
```
$ git clone git@github.com:BradyHammond/Reputation-API.git
$ cd Reputation-API
$ virtualenv -p python3 venv
$ source venv/bin/activate
$ pip3 install -r requirements.txt
$ gunicorn run:app
```
To stop the server type `Ctrl+C` in the command-line. To exit the virtual environment type `deactivate` in the command-line.
# Usage
POST requests to the API should be of the following format and hit the endpoint "/reputation":
```
{
  "reputer": "name_of_reputer",
  "reputee": "name_of_reputee",
  "repute":
  {
    "rid" : unique_identifier,
    "feature": "reach or clarity",
    "value": 0 to 10
  }
}
```
It is the client's responsibility to ensure that RIDs are unique. It is suggested that RID's be universally unique, but this is not strictly enforced. However, RID's must be unique per paring of reputer (client) and reputee (target) otherwise they will be discarded. The server will throw an HTTP 400 error if no JSON is sent, an empty JSON is sent, or a JSON with the wrong formatting is sent. The server will throw a 422 error if the JSON is incorrectly encoded. The server will return a 201 status if the posted data was successfully added to the database or a 200 status if the posted data was already found in the database. 

GET requests to the API should hit the enpoint "/reputation/{reputee}" and will return a JSON of the following format:
```
{
   "reputee": "name_of_reputee",
   "clout":
   {
     "score": number between 0 and 1,
     "confidence": number between 0 and 1
   },
   "reach":
   {
     "score": number between 0 and 10,
     "confidence": number between 0 and 1
   },
   "clarity":
   {
     "score": number between 0 and 10,
     "confidence": number between 0 and 1
   }
}
 ```
The server will throw a 400 error if no reputee query parameter is included in the URL or if the queried reputee cannot be found in the database. A successful GET request will return a 200 status and a JSON.
