FROM node:alpine

RUN apk update && apk add --no-cache git 

# Install dependencies
WORKDIR /build
COPY package.json yarn.lock /build/
RUN yarn install --frozen-lockfile --ignore-optional --ignore-scripts

# copy only required for the build files
COPY src /build/src
COPY webpack.config.ts tsconfig.json custom.d.ts /build/
COPY typings/styled-patch.d.ts /build/typings/styled-patch.d.ts

RUN npm run bundle:standalone

FROM nginx:alpine

ENV PAGE_TITLE="Cervezas API"
ENV PAGE_FAVICON="favicon.png"
ENV SPEC_URL="http://0.0.0.0:5000/documentation"
ENV PORT=80
ENV REDOC_OPTIONS=

# copy files to the nginx folder
COPY --from=0 build/bundles /usr/share/nginx/html
COPY config/docker/index.tpl.html /usr/share/nginx/html/index.html
COPY demo/favicon.png /usr/share/nginx/html/
COPY config/docker/nginx.conf /etc/nginx/
COPY config/docker/docker-run.sh /usr/local/bin

EXPOSE 80

CMD ["sh", "/usr/local/bin/docker-run.sh"]