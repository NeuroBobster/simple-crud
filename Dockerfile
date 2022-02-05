FROM python:3.8.10

# set a directory for the app
WORKDIR /project

# copy just the requirements
COPY ./requirements.txt /project/requirements.txt

# install dependencies
RUN pip install --no-cache-dir --upgrade -r /project/requirements.txt

# copy the project files
COPY ./app /project/app

# run the command
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]