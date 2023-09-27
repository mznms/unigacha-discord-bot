FROM python:slim
WORKDIR /work
COPY requirements.txt /work/
RUN pip install -r requirements.txt
COPY . /work
CMD python main.py
