# Hubcare - API

[![build status](https://gitlab.com/cjjcastro/2019-1-hubcare-api/badges/master/pipeline.svg)](https://gitlab.com/cjjcastro/2019-1-hubcare-api/pipelines)
[![Coverage Status](https://coveralls.io/repos/github/fga-eps-mds/2019.1-hubcare-api/badge.svg?branch=29-setup_ci_pipeline)](https://coveralls.io/github/fga-eps-mds/2019.1-hubcare-api?branch=29-setup_ci_pipeline)
[![Maintainability](https://api.codeclimate.com/v1/badges/956d64084dec1bc50ad3/maintainability)](https://codeclimate.com/github/fga-eps-mds/2019.1-hubcare-api/maintainability)
[![Average time to resolve an issue](http://isitmaintained.com/badge/resolution/fga-eps-mds/2019.1-hubcare-api.svg)](http://isitmaintained.com/project/fga-eps-mds/2019.1-hubcare-api "Average time to resolve an issue")
[![Percentage of issues still open](http://isitmaintained.com/badge/open/fga-eps-mds/2019.1-hubcare-api.svg)](http://isitmaintained.com/project/fga-eps-mds/2019.1-hubcare-api "Percentage of issues still open")
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

The Hubcare is an open-source project intended to help free software users and potential contributors to decide which repositories they should use or on which they should contribute. It has an API that pulls data from GitHub API and post it to a [Add-on](https://github.com/fga-eps-mds/2019.1-hubcare-plugin). Any more details about project may be found on [Documentation](https://cjjcastro.gitlab.io/2019-1-hubcare-docs/), which is mostly in Portuguese, due to Brazilian project stakeholders.

This repository, in special, is fully dedicated to the maintain API details. Feel free to read, run and contribute.

## Technologies

<img src="docs/images/django-rest-framework.png" alt="DjangoRest" height="100" width="110"/><img src="docs/images/chrome.gif" alt="Chrome" height="100" width="110"/><img src="docs/images/vscode.png" alt="Vscode" height="100" width="110"/><img src="docs/images/docker.gif" alt="Docker" height="100" width="110"/><img src="docs/images/github.gif" alt="Github" height="100" width="110"/>

## Installation

### Installing from Chrome Store

Just go to HubCare's page on [Chrome Store](https://chrome.google.com/webstore/detail/hubcare/oilkenamijbelpchecmfpllponcmlcbm) and be happy :wink:

### Running things locally

Wanna see it working on your machine, uh?

Unfortunately, the Add-on code wasn't made for local interaction, you may want to up the API on some deploy service to see it working. But you can still run the API and the Add-On separately if you want.

You'll need have [Docker](https://docs.docker.com/install/) and [Docker-Compose](https://docs.docker.com/compose/install/) installed to see the magic happenning.

And I just know how to do it on a Linux machine. C'mon, Windows is just for gaming, y'know. And MacOS users surely can pay someone to discover how to do it.

#### Running the API

Downloading

```bash
cd ~/your/directory/
git clone https://github.com/fga-eps-mds/2019.1-hubcare-api.git
cd 2019.1-hubcare-api
```

The HubCare API need to send a GitHub username and an API token to authenticate on GitHub API. This is set by environment variables as shown below. You can generate tokens [here](https://github.com/settings/tokens).

```bash
export NAME='username'
export TOKEN='token'
```

There you go!

```bash
docker-compose build
docker-compose up
```

If everything was done right, you now have the HubCare running on your machine. Just navigate to `0.0.0.0:8000` and you should see something. There are services running on ports [8000..8003].

Test it on http://0.0.0.0:8000/hubcare_indicators/fga-eps-mds/2019.1-hubcare-api

**Obs:** If you ever need to change the values of `NAME` or `TOKEN`, rerun `docker-compose build`. Those variables are got in build time.

#### Running the Add-on

Downloading

```bash
cd ~/your/directory/
git clone https://github.com/fga-eps-mds/2019.1-hubcare-plugin.git
cd 2019.1-hubcare-plugin
```

Building and uping things:

```bash
docker-compose build
docker-compose up
```

This should be enough to turn the service on ( ͡° ͜ʖ ͡°).

Then, open Google Chrome on [chrome://extensions/](chrome://extensions/), activate `Developer mode` on top right corner.

![Developer Mode](docs/images/chromeext.png)

You now shoud see hubcare extension, just activate it.

Just go to some GitHub repo to see it working. I recommend [this one](https://github.com/fga-eps-mds/2019.1-hubcare-api), you can even give it a star! :wink:

#### Running the... Docs?

Okay, I undertand, you don't believe on internet info, wanna see it on your own machine, right?

There you go then

```bash
cd ~/your/directory/
git clone https://github.com/fga-eps-mds/2019.1-hubcare-docs.git
cd 2019.1-hubcare-docs
```

Yeah, now run the docs, girl! Run the docs, boy!

```bash
docker-compose up --build
```

Now, [localhost:8000](localhost:8000) should have a beautyful documentation page.

**Obs:** If you ever want to contribute to docs, make sure to check if the MKDocs is rendering as you wish with the proceed above.

## Deployment

It's set on [GitLab](https://gitlab.com/cjjcastro/2019-1-hubcare-api), so we can use GitLab CI.

## Built With 

[Djago Rest Framework](https://www.django-rest-framework.org/)

## Contributing

Please make sure to read the [Contributing Guide](https://github.com/fga-eps-mds/2019.1-hubcare-api/blob/master/.github/CONTRIBUTING.md) before making a pull request. After you've read, don't forget to take an issue!

## Testing

### Unit Test

To execute all tests:

```shell
make test
```

To get a [Coveralls] report:

```shell
make coverage report
```

### Style Checking

```shell
make style
```

## License

Do whatever you want with this code, bro/sis. This is under [MIT License](./LICENSE).