FROM golang:latest

WORKDIR /home

COPY main.go .

RUN go build main.go

CMD ./main
