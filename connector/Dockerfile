# mcp-front (pinned commit + local patch) + garmin-personal-mcp (hash-locked dependencies).
# Build:  podman build -t garmin-mcp:0.1 connector/     (or docker build)
ARG MCP_FRONT_COMMIT=a6f59b103afdd3fd2c20eb3e32e2e1dc50bc5282

FROM golang:1.25-alpine AS build
ARG MCP_FRONT_COMMIT
RUN apk add --no-cache git patch
WORKDIR /src
RUN git init -q . \
 && git remote add origin https://github.com/stainless-api/mcp-front.git \
 && git fetch -q --depth 1 origin "${MCP_FRONT_COMMIT}" \
 && git checkout -q FETCH_HEAD
COPY patches/ /patches/
RUN patch -p1 < /patches/allow-any-domain.patch
RUN go mod download && go mod verify
RUN CGO_ENABLED=0 go build -trimpath -ldflags='-w -s' -o /out/mcp-front ./cmd/mcp-front

FROM python:3.12-slim
RUN useradd --system --uid 1001 --no-create-home --shell /usr/sbin/nologin mcp
COPY requirements.lock /tmp/requirements.lock
RUN pip install --no-cache-dir --require-hashes --no-deps -r /tmp/requirements.lock && rm /tmp/requirements.lock
COPY --from=build /out/mcp-front /usr/local/bin/mcp-front
COPY garmin-run.sh /usr/local/bin/garmin-run
COPY config.json /app/config.json
RUN chmod 755 /usr/local/bin/garmin-run
USER 1001
WORKDIR /app
EXPOSE 8080
ENTRYPOINT ["mcp-front", "-config", "/app/config.json"]
