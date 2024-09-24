=============================================
Data Engineering and API Development Exercise
=============================================

Task Description
----------------

Develop a pipeline that involves setting up a MongoDB database using Docker Compose, 
retrieving and storing data from an external API, and exposing this data through FastAPI. 

1. Setup MongoDB with Docker Compose
Use Docker Compose to set up a MongoDB database.

2. Data Retrieval and Loading into MongoDB
Retrieve data from the JSONPlaceholder - Free Fake REST API and store it in MongoDB with python.

3. Create a RESTful API with FastAPI
Develop a FastAPI application to provide access to the mongo data. 
Include an endpoint to report the total number of posts and comments for each user.


Local Development
-----------------

To create a virtual environment:

.. code-block:: bash

    pyenv install 3.12.3
    pyenv local 3.12.3
    python3 -m venv .venv
    source .venv/bin/activate

To install the dependencies:

.. code-block:: bash

    pip install -r requirements.txt


To run MongoDB locally, you can use Docker. 
MongoDB will be available at `mongodb://root:example@localhost:27017`.:

.. code-block:: bash

    docker compose up -d


To run the application, use Uvicorn. 
The API documentation will be available at `http://localhost:8000/docs`:

.. code-block:: bash

    uvicorn app.main:app --reload


To run the data retrieval script:

.. code-block:: bash

    python data_retrieval/load_data.py

To tear down the MongoDB container, use the following command:

.. code-block:: bash

    docker compose down


