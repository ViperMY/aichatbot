# app/Dockerfile

FROM --platform=linux/amd64 python:3.9-slim

WORKDIR /momoChatBot    

COPY . .
RUN pip3 install -r requirements.txt

EXPOSE 8000

HEALTHCHECK CMD curl --fail http://localhost:8000/

ENTRYPOINT ["streamlit", "run", "chatBot.py", "--server.port=8000", "--server.address=0.0.0.0"]