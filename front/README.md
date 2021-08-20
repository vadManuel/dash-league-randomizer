# Frontend

## Before running

Make sure to have the following dependencies installed on your system:

- [Node.js](https://nodejs.org/en/download/)
- [Yarn](https://classic.yarnpkg.com/en/docs/install/#windows-stable)

## Local hosting of application

1. Install node dependencies

   ```bash
   yarn install
   ```

1. Start application

   ```bash
   yarn run start
   ```

## Structure

|                   |                                               |
| ----------------- | --------------------------------------------- |
| `scripts/`        | Contains all general scripts                  |
| `src/`            | Contains all of our react codebase            |
| `src/routes/`     | App navigation                                |
| `src/assets/`     | Images, icons, and other static files         |
| `src/containers/` | Wrapping components                           |
| `src/contexts/`   | React context                                 |
| `src/types/`      | Typescript related files or functions         |
| `src/utils/`      | Helper functions                              |
| `src/components/` | Contains all components that are not wrappers |
