FROM python:3.12.4
ENV PYTHONUNBUFFERED=1
WORKDIR /django
COPY requirements.txt requirements.txt
COPY ./entrypoint /entrypoint
RUN sed -i 's/\r$//g' /entrypoint
RUN chmod +x /entrypoint
RUN pip3 install -r requirements.txt
EXPOSE 8000
ENTRYPOINT ["/entrypoint"]
