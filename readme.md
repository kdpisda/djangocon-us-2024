# System Preparation for Tutorial

This guide will help you prepare your system for the upcoming tutorial by installing Poetry and Docker/Docker Compose.

## 1. Installing Poetry

Poetry is a tool for dependency management and packaging in Python.

### Installation Steps:

1. Open a terminal or command prompt.
2. Run the following command:

   ```
   curl -sSL https://install.python-poetry.org | python3 -
   ```

3. After installation, restart your terminal and verify the installation:

   ```
   poetry --version
   ```

## 2. Installing Docker and Docker Compose

Docker is a platform for developing, shipping, and running applications in containers. Docker Compose is a tool for defining and running multi-container Docker applications.

### Installation Steps:

1. Visit the official Docker website: [https://www.docker.com/get-started/](https://www.docker.com/get-started/)
2. Download and install Docker Desktop for your operating system (Windows, macOS, or Linux).
3. Docker Compose is included with Docker Desktop for Windows and macOS. For Linux, you may need to install it separately.
4. After installation, verify by running these commands in your terminal:

   ```
   docker --version
   docker compose --version
   ```

## Troubleshooting

If you encounter any issues during the installation process, please refer to the official documentation:

- [Poetry Documentation](https://python-poetry.org/docs/)
- [Docker Documentation](https://docs.docker.com/)

If you still need assistance, please reach out to me at [hello@kdpisda.in](mailto:hello@kdpisda.in).
