
# Start with the Python base image
FROM python:3.11-slim-buster AS python-base
WORKDIR /app
COPY ./ /app
RUN pip install --no-cache-dir -r requirements.txt

# Then use the Node.js base image
FROM node:17 AS node-base
WORKDIR /app
COPY ./xmtp-service/package*.json ./
RUN npm install
COPY ./xmtp-service .

# Final image
FROM debian:buster
RUN apt-get update && apt-get install -y supervisor curl

# Copy Python environment from python-base
COPY --from=python-base /usr/local /usr/local

# Copy Node.js environment from node-base
COPY --from=node-base /usr/local /usr/local

# Copy app files from python-base
COPY --from=python-base /app /app

# Copy app files from node-base
COPY --from=node-base /app /xmtp-service

# Copy supervisor configuration
COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf

CMD ["/usr/bin/supervisord"]
  