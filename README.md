# Overview
The reputation API is a simple API implemented using Python 3.6 and the Falcon API framework. It has a single endpoint ("/reputation") that can take either a POST or a GET method. Data sent in a POST to the API, simply gets stored in a database. Upon a GET request, data is pulled from the database, processed, and returned to the requester. Reputation data includes statistics about clarity, clout, and reach.
# Setup
To setup the API on your own computer you will first need [Python 3.6](https://www.python.org/downloads/). With your download of Python 3.6, there should have been a command-line tool installed on your computer called pip3. To check if pip3 was successfully installed on your machine, open a terminal (or command prompt if you're on Windows), and run one of the following commands: `pip3 -V` or `pip3 --version`. If you recieve an error message similar to this one: `bash: pip3: command not found`, run the command `sudo easy_install3 pip` (on Debian/Ubuntu distros of Linux, you may first have to run the command `sudo apt-get install python3-setuptools` before easy_install3 is available). For more information on downloading and installing pip3 visit [https://pip.pypa.io/en/stable/installing/](https://pip.pypa.io/en/stable/installing/). Once Python 3.6 and pip3 are both installed, you will also need virtualenv which is a Python module that let's you setup your own virtual environment. You can install [virtualenv](https://virtualenv.pypa.io/en/stable/) by running the command `pip3 install virtualenv` from the command-line.

With all the prerequisites downloaded and installed, you can now run the following set of commands to setup the API in a virtual environment:
```
$ git clone git@github.com:BradyHammond/Reputation-API.git
$ cd Reputation-API
$ virtualenv -p python3 venv
$ source venv/bin/activate
$ pip3 install -r requirements.txt
$ gunicorn run:app
```
To stop the server type `Ctrl+C` in the command-line. To exit the virtual environment type `deactivate` in the command-line.

Included with the API is basic unit testing. To run the provided unit tests ensure that your virtual environment is active and then run the command `python3 -m unittest tests/test_api.py`. There are currently 8 test cases. If a test case fails please create an issue in this git repository and include the failure message.
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
It is the client's responsibility to ensure that RIDs are unique. It is suggested that RID's be universally unique, but this is not strictly enforced. RID's must, however, be unique per paring of reputer (client) and reputee (target) otherwise they will be discarded. The server will throw an HTTP 400 error if no JSON is sent, an empty JSON is sent, or if a JSON with the wrong formatting is sent. The server will throw a 422 error if the JSON is incorrectly encoded. The server will return a 201 status if the posted data was successfully added to the database or a 200 status if the posted data was already found in the database. 

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
# Development
The API was designed with simplicity and clarity in mind. The project has 3 main parts: the api object, the processor object, and the storage object. The api object sets up the GET and POST routes for the api. For the most part the api object just handles data verification, although it does create an instance of a storage object for storing POST data and an instance of a processor object for retrieving and processing requested GET data. The processor is created to process GET requested data. It calculates the clarity, clout, and reach statistics for a given reputee. The storage object simply interfaces with the database (which is a Python shelve). The API can function in two modes: Development and Production. This ensures that the production and development databases are kept separate. The API has a run.py file that creates the api object to run on the server. The API also has a test_api.py file to unit test the API.

The statistics generated by the server are calculated in the following way:

| Statstic | Method |
| -------- | ------ |
| Reach Score |  The arithmetic average of all the unique reach POSTs connected with a given reputee. |
| Reach Confidence | The result of f(x,a,b) where a = 2, b = 6, and x = the total number of unique reach POSTs connected with a given reputee. |
| Clarity Score |  The arithmetic average of all the unique clarity POSTs connected with a given reputee. |
| Clarity Confidence | The result of f(x,a,b) where a = 4, b = 8, and x = the total number of unique clarity POSTs connected with a given reputee. |
| Clout Score | The normalized weighted average of the reach and clarity scores where the weights are the reach and clarity confidences. A normalized weight is computed by dividing each weight by the sum of the weights. A normalized weighted average is computed by summing the product of each normalized weight and score then dividing by 10. |
| Clout Confidence | The minimum of the reach and clarity confidences. |

![S function](https://www.ijser.org/paper/A-FUZZY-BASED-APPROACH-FOR-PRIVACY-PRESERVING-CLUSTERING/Image_001.png "S Function")
# Resources
I have tried to include everything needed for running, using, and understanding the Reputation API here, but you may still find the following resources useful:

| URL | Description |
| --- | ----------- |
| [https://www.python.org](https://www.python.org) | Python overview/documentation |
| [https://falconframework.org](https://falconframework.org) | Falcon overview/documentation |
| [http://falcon.readthedocs.io/en/stable/user/tutorial.html#testing-your-application](http://falcon.readthedocs.io/en/stable/user/tutorial.html#testing-your-application) | Falcon testing documentation |
| [http://falcon.readthedocs.io/en/stable/user/quickstart.html](http://falcon.readthedocs.io/en/stable/user/quickstart.html) | Falcon quickstart |
| [https://falcon.readthedocs.io/en/stable/user/tutorial.html](https://falcon.readthedocs.io/en/stable/user/tutorial.html) | Falcon tutorial |
| [https://brew.sh](https://brew.sh) | Hombrew overview/documentation (for installing Python 3.6 on MacOS) |
| [https://hurl.it](https://hurl.it) | Hurl (online GET and POST testing platform) |
| [https://insomnia.rest](https://insomnia.rest) | Insomnia Rest Client (desktop GET and POST testing platform) |
| [https://virtualenv.pypa.io/en/stable](https://virtualenv.pypa.io/en/stable) | virtualenv documentation |
| [https://gunicorn.org](http://gunicorn.org) | gunicorn documentation |
| [https://docs.python.org/3/library/unittest.html](https://docs.python.org/3/library/unittest.html) | unittest documentation |
| [https://pypi.python.org/pypi/ujson](https://pypi.python.org/pypi/ujson) | ujson documentation |
