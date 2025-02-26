# RestaurantBusiness

RestaurantBusiness is a web application that allows restaurant owners to manage their restaurants, create menus, and allow employees to vote for their favorite menus.

## Features

- Restaurant management
- Menu creation
- Voting system for employees

## Requirements

- Docker
- Docker Compose

## Installation

1. Clone the repository:

    ```sh
    git clone https://github.com/gashchukk/RestaurantBusiness.git
    cd RestaurantBusiness
    ```

2. Build and start the application using Docker Compose:

    ```sh
    docker-compose up --build
    ```

3. The application will be available at `http://127.0.0.1:8000`.

## Running Tests

1. To run the tests, use the following command:

    ```sh
    docker-compose run web pytest
    ```

## API Documentation

The API documentation is available at `http://127.0.0.1:8000/docs`.

## Alternative Installation (Without Docker)

1. Clone the repository:

    ```sh
    git clone https://github.com/gashchukk/RestaurantBusiness.git
    cd RestaurantBusiness
    ```

2. Create a virtual environment and activate it:

    ```sh
    python -m venv .venv
    source .venv/bin/activate
    ```

3. Install the dependencies:

    ```sh
    pip install -r requirements.txt
    ```

4. Set up the environment variables. Create a [.env](http://_vscodecontentref_/1) file in the root directory and add the following variables:

    ```env
    DATABASE_URL=postgresql://user:password@localhost/dbname
    SECRET_KEY=your_secret_key
    ACCESS_TOKEN_EXPIRE_MINUTES=30
    ```

5. Run the database migrations:

    ```sh
    alembic upgrade head
    ```

6. Start the FastAPI server:

    ```sh
    uvicorn app.main:app --reload
    ```

7. The application will be available at `http://127.0.0.1:8000`.

## License

This project is licensed under the MIT License.