FROM python:slim
COPY worker requirements worker/
RUN pip install -r worker/live
CMD python -m worker
