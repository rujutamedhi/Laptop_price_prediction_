# Use official Python image
#slim for lightweight
FROM python:3.10-slim


# Set working directory
# this will create app  (container)
WORKDIR /app

# Copy files
# first . for current local directory and second . for app folder
COPY . .

# Install dependencies
# --no-cache-dir to avoid caching - reducing space
RUN pip install --no-cache-dir -r requirements.txt

# Expose port
# just for documentation...not actually asking to use 5000 ..asked to use in next line
EXPOSE 5000

# Run the app using gunicorn (production-ready)
# first app refers to file name app.py and second to flask object app=Flask(__name__)
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]

RUN pip install mlflow 


#step 1
#to build image
# docker build -t ml-flask-app .
#-t stands for tag
#ml-flask-app is image name

#step 2
#to run container
#docker run --name my-flask-container -p 5000:5000 ml-flask-app
#-p is for port mapping
#5000 is local machine and 5000 is container port
