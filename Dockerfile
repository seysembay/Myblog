FROM tiangolo/uwsgi-nginx-flask:python3.11

COPY ./req.txt /app/req.txt

RUN pip install --no-cache-dir --upgrade -r /app/req.txt

COPY ./ /app