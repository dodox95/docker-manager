# Docker Manager

Docker Manager is a script-based application to simplify common Docker tasks, such as initializing projects, managing images and containers, and more.

## Structure

The main script is found in `main.py` which interfaces with utilities in `docker_utils.py` and `utils.py`.

docker_manager/
│
├── main.py # The main script that runs the application.
│
└── parts/ # Utility scripts to support the main application.
├── docker_utils.py # Contains functions for managing Docker.
└── utils.py # Helper functions and the main menu of the application.


## Features

1. Initialize Docker projects with single or multiple folder setups.
2. Check and install Docker (specifically for Ubuntu systems).
3. Search Docker Images on Docker Hub.
4. List all Docker images and containers.
5. Delete specific Docker images or containers.
6. Modify Dockerfiles by adding plugins/packages, searching Docker Hub, or importing a requirements file.
7. Build Docker images from Dockerfiles.

## Usage

1. Clone the repository.
2. Navigate to the directory containing `main.py`.
3. Run the script with `python3 main.py`.
4. Follow the on-screen instructions to perform various Docker tasks.


## Contribution

Feel free to contribute to this project by submitting pull requests or opening issues.

## License

This project is open-sourced under the MIT License.

