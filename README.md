# Hubcare - API

[![build status](https://gitlab.com/cjjcastro/2019-1-hubcare-api/badges/master/pipeline.svg)](https://gitlab.com/cjjcastro/2019-1-hubcare-api/pipelines)
[![Coverage Status](https://coveralls.io/repos/github/fga-eps-mds/2019.1-hubcare-api/badge.svg?branch=)](https://coveralls.io/github/fga-eps-mds/2019.1-hubcare-api?branch=)
[![Maintainability](https://api.codeclimate.com/v1/badges/956d64084dec1bc50ad3/maintainability)](https://codeclimate.com/github/fga-eps-mds/2019.1-hubcare-api/maintainability)
[![Average time to resolve an issue](http://isitmaintained.com/badge/resolution/fga-eps-mds/2019.1-hubcare-api.svg)](http://isitmaintained.com/project/fga-eps-mds/2019.1-hubcare-api "Average time to resolve an issue")
[![Percentage of issues still open](http://isitmaintained.com/badge/open/fga-eps-mds/2019.1-hubcare-api.svg)](http://isitmaintained.com/project/fga-eps-mds/2019.1-hubcare-api "Percentage of issues still open")
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

The Hubcare is an open-source project to manage if a repository is good or not to a newcomer, either a passing visitor, someone who looks for contributions or someone who just is interested in the software. If you are interested in the documentation, just go to [Hubcare Docs](https://fga-eps-mds.github.io/2019.1-hubcare-docs/)

This repository is the Hubcare's API, the bridge that communicates the github API and our chrome plugin.


## Getting Started

Pull the source code from master and run

```
$docker-compose build
$docker-compose up
```

Running this commands will set all the needed configuration and will start the server at the port 0.0.0.0

For development reason you must set environment variable.

```
export NAME='name'
export TOKEN='token'
```

## Contributing

Please make sure to read the [Contributing Guide]() before making a pull request. After you've read, don't forget to take an issue!

## License

[MIT](./LICENSE)

