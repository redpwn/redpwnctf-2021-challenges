FROM rust:1.53 AS builder

WORKDIR /app
COPY Cargo.lock .
COPY Cargo.toml .
RUN mkdir .cargo
RUN cargo vendor > .cargo/config

COPY . .
RUN sed -i 's/127\.0\.0\.1/0\.0\.0\.0/g' src/main.rs
RUN cargo build --release
