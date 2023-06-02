# start by pulling the python image
FROM python:3.10-bullseye

## copy the requirements file into the image
#COPY ./requirements.txt /app/requirements.txt
#
## switch working directory
#WORKDIR /app
#
## install the dependencies and packages in the requirements file
#RUN pip install -r requirements.txt
#
## copy every content from the local file to the image
#COPY . /app
#
## configure the container to run in an executed manner
#ENTRYPOINT [ "python" ]
#
#CMD ["main.py" ]


WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
RUN pip install pydevd-pycharm~=231.9011.38

COPY . .

CMD [ "python", "-m" , "flask", "run", "--host=0.0.0.0"]