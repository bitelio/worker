FROM python:slim
COPY requirements worker/requirements
RUN pip install -r worker/requirements/live
COPY worker worker/
CMD python -m worker
