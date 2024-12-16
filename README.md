This is the implementation for the Sano Interview take home test

It has been built using FastAPI to provide the endpoints, and uses a sqlite database for the storing and retrieving of user data.

#Usage
Install the requirements listed in requirements.txt:

    pip install -r requirements.txt

Then to run, simply execute:

    fastapi dev main.py

The endpoints are listed in endpoints/endpoints.py but they are:

##Retrieve all individuals uploaded:

    GET /individuals

##Retreive an individuals data:

    GET /individuals/{individual}/genetic-data?variants=rs123

Replace the `{individual}` with the name wanted.
The `variants` field is optional but will retrieve only those requested.

##Create individual

    POST /individuals

Providing a request body as `application/json` type of the form:
{
"name": "<desired_name>"
}

##Insert individuals data

    POST /indiivudals/{individual_id}/genetic_data

Providing a request body as a multipart/form-data containing the file data to be uploaded.

#Further improvements

Currently there is limited checking on the data. If one field is empty, then the whole file is not uploaded, which may not be the desired outcome.

Further testing could be implemented to think of further corner cases and scenarios in which the data could be inserted incorrectly, and performance could be improved by using threading if many users were going to be uploading and retrieiving data.
