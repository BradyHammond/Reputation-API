# ================================================== #
#                         API                        #
# ================================================== #
# Author: Brady Hammond                              #
# Created: 12/01/2017                                #
# Last Edited: N/A                                   #
# Last Edited By: N/A                                #
# ================================================== #
#                      IMPORTS                       #
# ================================================== #


from app.api.processor import Processor
from app.storage.storage import Data
import falcon

# If ujson is availalbe use it (it has better
# performance than Python's standard json library,
# and while the performance enhancements might be
# negligible at this time, using ujson will add
# scalability if the API is ever expanded),
# otherwise use the standard json library.
try:
    import ujson as json
except ImportError:
    import json


# ================================================== #
#                  CLASS DEFINITIONS                 #
# ================================================== #


# Define reputation API object
class ReputationAPI(object):

    # Define init function
    def __init__(self, mode="Production"):
        self.mode = mode

    # ============================================= #

    # Define handler for GET request
    def on_get(self, req, resp, reputee=None):
        # Check for query parameter
        if reputee is None:
            # If no query parameter is found, output 400 error
            raise falcon.HTTPError(falcon.HTTP_400, 'Error', 'A valid query is required.')

        # Set a boolean to check for reputee in database
        reputee_found = False
        # Open database
        data = Data(self.mode)
        data.open()

        # Look through database to see if any reputees match query
        for key in data.db:
            if data.db[key]['reputee'] == reputee:
                # If a matching reputee is found, record that reputee is found and exit loop
                reputee_found = True
                break

        # Close database
        data.close()

        # Check if any reputees matching query were found
        if not reputee_found:
            # If no reputees matching query were found, output 400 error
            raise falcon.HTTPError(falcon.HTTP_400, 'Error', 'Reputee could not be found.')

        # Process query request
        processor = Processor(reputee, self.mode)
        processed_data = processor.get_all()

        # Return processed data
        resp.status = falcon.HTTP_200
        resp.body = json.dumps({"reputee": reputee, "clout": {
            "score": processed_data[0][0],
            "confidence": processed_data[0][1]}, "reach": {
            "score": processed_data[1][0],
            "confidence": processed_data[1][1]}, "clarity": {
            "score": processed_data[2][0],
            "confidence": processed_data[2][1]}})

    # ============================================= #

    # Define handler for POST request
    def on_post(self, req, resp):
        # Falcon has some built in validation with
        # req.media, but implementing the validation
        # manually allows for use of ujson.
        # It also allows for verification that the
        # posted json has the correct fields.

        # Check that posted json is readable
        try:
            raw_json = req.stream.read()

            # Check that posted json has content
            if not raw_json:
                # If no content is present, output 400 error
                raise falcon.HTTPError(falcon.HTTP_400, 'Error', 'A valid JSON document is required.')
        except Exception:
                # If json is unreadable output 400 error
                raise falcon.HTTPError(falcon.HTTP_400, 'Error', 'A valid JSON document is required.')

        # Check if posted json is encoded correctly
        try:
            json_object = json.loads(raw_json)
        except ValueError:
            # If json is encoded incorrectly, output 422 error
            raise falcon.HTTPError(falcon.HTTP_422, 'Malformed JSON',
                                   'Could not decode the request body. The '
                                   'JSON was incorrect or not encoded as '
                                   'UTF-8.')

        # Check if posted json is formatted correctly
        try:
            reputer = json_object['reputer']
            reputee = json_object['reputee']
            rid = str(json_object['repute']['rid'])
            feature = json_object['repute']['feature']
            value = json_object['repute']['value']
        except KeyError:
            # If json is formatted incorrectly, output 400 error
            raise falcon.HTTPError(falcon.HTTP_400, 'Malformed JSON',
                                   'Could not decode the request body. The '
                                   'JSON was formatted incorrectly.')

        # Open database
        data = Data(self.mode)
        data.open()

        # Check if posted data is a duplicate
        if (rid+"-"+reputer+"-"+reputee) not in data.db:
            # If posted data is not a duplicate, add data to database
            data.db[rid+"-"+reputer+"-"+reputee] = {"reputer": reputer,
                            "reputee": reputee,
                            "repute": {"rid": rid, "feature": feature, "value": value}}
            # Close database
            data.close()
            # Return a 201 status
            resp.status = falcon.HTTP_201
            resp.body = json.dumps({'message': 'rid-' + rid + ' successfully created.'})

        else:
            # Close database
            data.close()
            # Return a 200 status
            resp.status = falcon.HTTP_200
            resp.body = json.dumps({'message': 'rid-' + rid + ' already exists.'})


# ================================================== #
#                        EOF                         #
# ================================================== #
