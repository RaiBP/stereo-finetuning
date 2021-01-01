#FROM gcr.io/google-appengine/python
#LABEL python_version=python3.7
#RUN apt-get update \
# && apt-get install -y ffmpeg libsm6 libxext6
#COPY requirements.txt /app/
#RUN /opt/python3.7/bin/python3.7 -m pip install --upgrade pip
#RUN pip3 install -r requirements.txt
#COPY . /app/
#EXPOSE 8050
#CMD ["gunicorn", "-b", ":8050", "app:server"]

FROM gcr.io/google-appengine/python

# Create a virtualenv for dependencies. This isolates these packages from
# system-level packages.
# Use -p python3 or -p python3.7 to select python version. Default is version 2.
RUN virtualenv /env -p python3.7

# Setting these environment variables are the same as running
# source /env/bin/activate.
ENV VIRTUAL_ENV /env
ENV PATH /env/bin:$PATH

# Copy the application's requirements.txt and run pip to install all
# dependencies into the virtualenv.
RUN apt-get update \
 && apt-get install -y ffmpeg libsm6 libxext6
ADD requirements.txt /app/requirements.txt
RUN /env/bin/python -m pip install --upgrade pip
RUN pip install -r /app/requirements.txt

# Add the application source code.
ADD . /app
WORKDIR /app
# Run a WSGI server to serve the application. gunicorn must be declared as
# a dependency in requirements.txt.

EXPOSE 8050
ENTRYPOINT ["gunicorn", "-b", ":8050", "app:server"]