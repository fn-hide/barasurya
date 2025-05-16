# Barasurya

<a href="https://github.com/fn-hide/barasurya/actions?query=workflow%3ATest" target="_blank"><img src="https://github.com/fn-hide/barasurya/workflows/Test/badge.svg" alt="Test"></a>
<a href="https://coverage-badge.samuelcolvin.workers.dev/redirect/fn-hide/barasurya" target="_blank"><img src="https://coverage-badge.samuelcolvin.workers.dev/fn-hide/barasurya.svg" alt="Coverage"></a>


<div align="center">
  <p>
    <a href="https://github.com/fn-hide/barasurya" target="_blank">
      <img width="100%" src="./img/barasurya-wide.png" alt="Barasurya banner"></a>
  </p>
</div>

## Technology Stack and Features

- ⚡ [**FastAPI**](https://fastapi.tiangolo.com) for the Python backend API.
    - 🧰 [SQLModel](https://sqlmodel.tiangolo.com) for the Python SQL database interactions (ORM).
    - 🔍 [Pydantic](https://docs.pydantic.dev), used by FastAPI, for the data validation and settings management.
    - 💾 [PostgreSQL](https://www.postgresql.org) as the SQL database.
- 🚀 [React](https://react.dev) for the frontend.
    - 💃 Using TypeScript, hooks, Vite, and other parts of a modern frontend stack.
    - 🎨 [Chakra UI](https://chakra-ui.com) for the frontend components.
    - 🤖 An automatically generated frontend client.
    - 🧪 [Playwright](https://playwright.dev) for End-to-End testing.
    - 🦇 Dark mode support.
- 🐋 [Docker Compose](https://www.docker.com) for development and production.
- 🔒 Secure password hashing by default.
- 🔑 JWT (JSON Web Token) authentication.
- 📫 Email based password recovery.
- ✅ Tests with [Pytest](https://pytest.org).
- 📞 [Traefik](https://traefik.io) as a reverse proxy / load balancer.
- 🚢 Deployment instructions using Docker Compose, including how to set up a frontend Traefik proxy to handle automatic HTTPS certificates.
- 🏭 CI (continuous integration) and CD (continuous deployment) based on GitHub Actions.

## Documentations

- General Development: [development.md](./development.md).
- Backend: [backend/README.md](./backend/README.md).
- Frontend: [frontend/README.md](./frontend/README.md).
- Deployment: [deployment.md](./deployment.md).

## Release Notes

Check the file [release-notes.md](./release-notes.md).

## License

The Full Stack FastAPI Template is licensed under the terms of the MIT license.
