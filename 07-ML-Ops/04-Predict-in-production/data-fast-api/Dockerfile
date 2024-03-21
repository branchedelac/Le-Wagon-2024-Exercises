FROM python:3.10.6-buster

COPY requirements_prod.txt /requirements_prod.txt
COPY setup.py setup.py

RUN pip install --upgrade pip
RUN pip install -r requirements_prod.txt

COPY taxifare taxifare
RUN pip install .

COPY Makefile Makefile
RUN make reset_local_files

CMD uvicorn taxifare.api.fast:app --host 0.0.0.0 --port $PORT
