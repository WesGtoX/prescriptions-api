<h1 align="center">
  Prescriptions API
  <br />
</h1>

<p align="center">
  <a href="#about-the-project">About</a>&nbsp;&nbsp;|&nbsp;&nbsp;
  <a href="#technology">Technology</a>&nbsp;&nbsp;|&nbsp;&nbsp;
  <a href="#getting-started">Getting Started</a>&nbsp;&nbsp;|&nbsp;&nbsp;
  <a href="#usage">Usage</a>&nbsp;&nbsp;|&nbsp;&nbsp;
  <a href="#roadmap">Roadmap</a>&nbsp;&nbsp;|&nbsp;&nbsp;
  <a href="#license">License</a>
</p>

<p align="center">
  <img alt="Prescriptions API CI" src="https://github.com/WesGtoX/prescriptions-api/actions/workflows/fastapi-app.yml/badge.svg" />
  <img alt="GitHub top language" src="https://img.shields.io/github/languages/top/wesgtox/prescriptions-api?style=plastic" />
  <img alt="GitHub language count" src="https://img.shields.io/github/languages/count/wesgtox/prescriptions-api?style=plastic" />
  <img alt="GitHub last commit" src="https://img.shields.io/github/last-commit/wesgtox/prescriptions-api?style=plastic" />
  <img alt="GitHub issues" src="https://img.shields.io/github/issues/wesgtox/prescriptions-api?style=plastic" />
  <img alt="License" src="https://img.shields.io/github/license/wesgtox/prescriptions-api?style=plastic" />
</p>


## About the Project

Prescription API is a medical prescription service, which inserts new prescriptions and integrates with another service that has four endpoints:
- `[GET] /physicians/:id/`: returns the data of a specific physician by its `ID`.
- `[GET] /clinics/:id/`: returns the data of a specific clinic by its `ID`.
- `[GET] /patients/:id/`: returns the data of a specific patient by their `ID`.
- `[POST] /metrics/`: final data integration, where the fetched data will be saved.


## Technology

This project was developed with the following technologies:

- [Python](https://www.python.org/)
- [FastAPI](https://fastapi.tiangolo.com/)
- [Docker](https://www.docker.com/)
- [Docker Compose](https://docs.docker.com/compose/)


## Getting Started

### Prerequisites

- [Python](https://www.python.org/downloads/)
- [Docker](https://docs.docker.com/get-started/)
- [Docker Compose](https://docs.docker.com/compose/install/)


### Install and Run

1. Clone the repository:
```bash
git clone https://github.com/WesGtoX/prescriptions-api.git
```
2. Set the environment variables:
```bash
cp .env.sample .env
```

#### Run using Docker and Docker Compose

1. Run:
```bash
make run
```
2. Run tests:
```bash
make test
```


## Usage

[Prescriptions Documentation]()


## Roadmap

See the [open issues](https://github.com/WesGtoX/prescriptions-api/issues) for a list of proposed features (and known issues).


## License

Distributed under the MIT License. See [LICENSE](LICENSE) for more information.

---

Made with ♥ by [Wesley Mendes](https://wesleymendes.com.br/) :wave:
