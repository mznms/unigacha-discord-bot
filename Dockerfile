FROM python:3.11-slim
RUN apt install -y tzdata \
  && ln -sf /usr/share/zoneinfo/Asia/Tokyo /etc/localtime
WORKDIR /work
COPY requirements.txt /work/
RUN pip install -r requirements.txt
COPY . /work
CMD python main.py
