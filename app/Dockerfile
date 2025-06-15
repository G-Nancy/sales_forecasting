#Use an official Python runtime as a parent image. The slim variant is a lightweight version of the full Python image, optimized for size but still suitable for running Python applications.
FROM python:3.9-slim

#The WORKDIR instruction creates a directory /app inside the container (if it doesn’t exist) and sets it as the working directory. Any following instructions (like COPY or RUN) will be executed relative to this directory.
WORKDIR /app

#This copies everything in the current directory (denoted by .) on your local machine to the /app directory inside the Docker container.
COPY . /app

# This command runs pip install to install the Python packages specified in the requirements.txt file (such as Flask, NumPy, or any other libraries needed by your app).
RUN pip install --no-cache-dir -r requirements.txt

#This tells Docker that the application inside the container will be running on port 5000 (which is the default port for Flask apps).
EXPOSE 5000

#This command starts the Flask app server using the flask run command. The option --host=0.0.0.0 ensures that Flask is accessible from outside the container (e.g., from the host machine or internet).
CMD ["flask", "run", "--host=0.0.0.0"]