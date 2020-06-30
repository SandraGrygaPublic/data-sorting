FROM python:3.6.10-slim-buster AS test-image

COPY ["app", "/app"]
COPY ["scripts", "/scripts"]
COPY ["tests", "/tests"]

RUN scripts/install-required-packages.sh 'app'
RUN scripts/run-tests.sh && cd app && python setup.py install

FROM python:3.6.10-slim-buster AS runtime-image
COPY --from=test-image /usr/local /usr/local
ENTRYPOINT ["generate-and-sort-file.sh"]
CMD ["5"]