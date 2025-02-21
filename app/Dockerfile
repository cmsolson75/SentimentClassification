FROM golang:1.23 AS builder

WORKDIR /app

COPY go.mod go.sum ./
RUN go mod tidy

COPY . .

RUN CGO_ENABLED=0 GOOS=linux GOARCH=amd64 go build -o sentiment-tui

FROM alpine:latest

WORKDIR /root/

COPY --from=builder /app/sentiment-tui .

RUN chmod +x /root/sentiment-tui

ENV API_URL="http://api:8000/predict"
ENV TERM=xterm-256color

CMD ["/bin/sh", "-c", "exec ./sentiment-tui"]