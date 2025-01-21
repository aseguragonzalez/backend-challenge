# Slack mock (WireMock)

WireMock's [project page](http://wiremock.org/docs/).

## How to build and run

```bash
docker run --rm -it -p 8080:8080 -p 8443:8443 $(docker build -q .)
```

## Authentication

To perform any authenticated request it is required to use the header "Authentication" with the value `Bearer 2S2KWJwabXXFz6Z7xXwibw4C7D4`.
