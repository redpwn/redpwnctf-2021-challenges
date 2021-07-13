FROM golang:1.16.5 AS builder

WORKDIR /wtjs
COPY go.mod go.sum ./

RUN go mod download && go mod verify

COPY . .

RUN CGO_ENABLED=0 go build -v

FROM gcr.io/distroless/static:latest as run

COPY --from=builder /wtjs/wtjs .

ENV PORT=8080
EXPOSE 8080
CMD ["/wtjs"]
