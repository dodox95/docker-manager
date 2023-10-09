import os

def check_and_install_docker():
    response = os.system("docker -v")
    if response == 0:
        print("Docker already installed!")
    else:
        print("Installing Docker...")
        os.system("sudo apt-get update")
        os.system("sudo apt-get install docker.io -y")
        print("Docker installed successfully!")


def initialize_docker_project():
    folder_choice = input("How many folders do you want to create (1/2): ")
    if folder_choice == '1':
        single_folder_setup()
    elif folder_choice == '2':
        two_folder_setup()
    else:
        print("Invalid choice!")
        initialize_docker_project()

def single_folder_setup():
    folder_name = input("Enter folder name: ")
    os.makedirs(folder_name)
    os.makedirs(os.path.join(folder_name, 'app'))
    with open(os.path.join(folder_name, 'app', 'dockerfile'), 'w') as f:
        f.write("""FROM ubuntu:latest
# Installing Node.js and npm
RUN apt-get update && apt-get install -y curl
RUN curl -fsSL https://deb.nodesource.com/setup_16.x | bash -
RUN apt-get install -y nodejs
CMD ['echo', 'Hello, Docker!']
""")


def two_folder_setup():
    main_folder_name = input("Enter main folder name: ")
    os.makedirs(main_folder_name)
    os.makedirs(os.path.join(main_folder_name, 'backend'))
    os.makedirs(os.path.join(main_folder_name, 'frontend'))
    with open(os.path.join(main_folder_name, 'docker-compose.yml'), 'w') as f:
        f.write("""
version: '3'
services:
  backend:
    build: ./backend
  frontend:
    build: ./frontend
""")
    with open(os.path.join(main_folder_name, 'backend', 'dockerfile'), 'w') as f:
        f.write("""FROM ubuntu:latest
# Installing Node.js and npm
RUN apt-get update && apt-get install -y curl
RUN curl -fsSL https://deb.nodesource.com/setup_16.x | bash -
RUN apt-get install -y nodejs
CMD ['echo', 'Hello, Backend!']
""")
    with open(os.path.join(main_folder_name, 'frontend', 'dockerfile'), 'w') as f:
        f.write("""FROM ubuntu:latest
# Installing Node.js and npm
RUN apt-get update && apt-get install -y curl
RUN curl -fsSL https://deb.nodesource.com/setup_16.x | bash -
RUN apt-get install -y nodejs
CMD ['echo', 'Hello, Frontend!']
""")

def search_docker_images():
    query = input("Search Docker Images (https://hub.docker.com/search?q=): ")
    os.system(f"xdg-open 'https://hub.docker.com/search?q={query}'")

def list_docker_images():
    os.system("sudo docker images")

def list_docker_containers():
    print("Listing all Docker containers...\n")
    os.system("sudo docker ps -a")

def delete_docker_image():
    print("Listing current Docker images...\n")
    result = os.popen("sudo docker images").read().strip().split('\n')
    images = result[1:]

    for i, image in enumerate(images, 1):
        print(f"{i}. {image}")

    try:
        choice = int(input("\nEnter the number of the REPOSITORY:TAG or IMAGE ID you want to delete: "))
        if 0 < choice <= len(images):
            image_parts = images[choice-1].split()
            image_id = image_parts[2]
            response = os.system(f"sudo docker rmi {image_id}")
            if response == 0:
                print(f"Successfully removed image {image_id}")
            else:
                print(f"Failed to delete the image {image_id}. There might be other dependencies using it.")
        else:
            print("Invalid choice!")
            delete_docker_image()
    except ValueError:
        print("Invalid input. Please enter a valid number.")
        delete_docker_image()

def delete_docker_container():
    print("Listing current Docker containers...\n")
    result = os.popen("sudo docker ps -a").read().strip().split('\n')
    containers = result[1:]

    for i, container in enumerate(containers, 1):
        print(f"{i}. {container}")

    try:
        choice = int(input("\nEnter the number of the CONTAINER ID you want to delete: "))
        if 0 < choice <= len(containers):
            container_parts = containers[choice-1].split()
            container_id = container_parts[0]
            response = os.system(f"sudo docker rm {container_id}")
            if response == 0:
                print(f"Successfully removed container {container_id}")
            else:
                print(f"Failed to delete the container {container_id}. It might be still running or has other issues.")
        else:
            print("Invalid choice!")
            delete_docker_container()
    except ValueError:
        print("Invalid input. Please enter a valid number.")
        delete_docker_container()

def find_dockerfiles(directory="."):
    dockerfiles = []
    for root, _, files in os.walk(directory):
        for file in files:
            if file.lower() == "dockerfile":
                dockerfiles.append(os.path.join(root, file))
    return dockerfiles

def modify_dockerfile():
    dockerfiles = find_dockerfiles()

    if not dockerfiles:
        print("No Dockerfiles found in the current directory!")
        return

    print("Select a Dockerfile:")
    for index, dockerfile in enumerate(dockerfiles, 1):
        print(f"{index}. {dockerfile}")

    try:
        choice = int(input("Enter the number of the Dockerfile you want to modify: "))
        if 1 <= choice <= len(dockerfiles):
            selected_dockerfile = dockerfiles[choice - 1]

            print("1. Add a predefined plugin/package")
            print("2. Search for a plugin or image on Docker Hub")
            print("3. Import requirements.txt")
            sub_choice = input("Enter your choice: ")

            if sub_choice == '1':
                print("Available plugins/packages:")
                for index, plugin in enumerate(PLUGINS, 1):
                    print(f"{index}. {plugin}")

                plugin_choice = int(input("Enter the number of the plugin/package you want to add: "))
                if 1 <= plugin_choice <= len(PLUGINS):
                    selected_plugin = PLUGINS[plugin_choice - 1]
                    with open(selected_dockerfile, "a") as df:
                        df.write(f"\n# Install {selected_plugin}\nRUN apt-get install -y {selected_plugin}\n")
                    print(f"{selected_plugin} added to {selected_dockerfile}!")
                else:
                    print("Invalid choice!")
                    return

            elif sub_choice == '2':
                search_term = input("Enter the name of the plugin or image you want to search for on Docker Hub: ")
                results = search_docker_hub(search_term)
                if results:
                    for index, result in enumerate(results, 1):
                        print(f"{index}. {result['name']} - {result['description']}")

                    result_choice = int(input("Enter the number of the result you want to add: "))
                    if 1 <= result_choice <= len(results):
                        selected_result = results[result_choice - 1]['name']
                        with open(selected_dockerfile, "a") as df:
                            df.write(f"\n# Install {selected_result}\nRUN apt-get install -y {selected_result}\n")
                        print(f"{selected_result} added to {selected_dockerfile}!")
                    else:
                        print("Invalid choice!")
                        return
                else:
                    print("No results found!")
                    return

            elif sub_choice == '3':
                dockerfile_directory = os.path.dirname(selected_dockerfile)
                txt_files = [f for f in os.listdir(dockerfile_directory) if f.endswith('.txt')]

                if not txt_files:
                    print("No .txt files found in the selected Dockerfile directory!")
                    return

                print("Select a requirements file:")
                for index, txt_file in enumerate(txt_files, 1):
                    print(f"{index}. {txt_file}")

                requirements_choice = int(input("Enter the number of the requirements file you want to import: "))
                if 1 <= requirements_choice <= len(txt_files):
                    selected_requirements = txt_files[requirements_choice - 1]
                    append_content = f"""
# Install Python requirements
COPY {selected_requirements} .
RUN pip install -r {selected_requirements}
"""
                    with open(selected_dockerfile, "a") as df:
                        df.write(append_content)
                    print(f"{selected_requirements} added to {selected_dockerfile}!")
                else:
                    print("Invalid choice!")
                    return

            else:
                print("Invalid choice!")
                return

        else:
            print("Invalid choice!")
    except ValueError:
        print("Invalid input. Please enter a valid number.")




def build_docker_image():
    dockerfiles = find_dockerfiles()

    if not dockerfiles:
        print("No Dockerfiles found.")
        return

    for index, dockerfile in enumerate(dockerfiles, 1):
        print(f"{index}. {dockerfile}")
    choice = int(input("Enter the number of the Dockerfile you want to build: "))

    if choice < 1 or choice > len(dockerfiles):
        print("Invalid choice.")
        return

    selected_dockerfile = dockerfiles[choice-1]
    confirm = input(f"Do you want to build this Dockerfile '{selected_dockerfile}'? (y/n): ")
    
    if confirm.lower() != 'y':
        return
    
    image_name = input("Enter the name for the Docker image (e.g., my_image:latest): ").strip()
    
    if not image_name:
        print("Image name is required.")
        return

    # Getting the directory of the Dockerfile.
    dockerfile_directory = os.path.dirname(selected_dockerfile)

    # Building the image.
    response = os.system(f"docker build -t {image_name} -f {selected_dockerfile} {dockerfile_directory}")
    
    # Checking for "npm: not found" error
    if response != 0:
        with open(selected_dockerfile, 'r') as df:
            content = df.read()
            if "npm: not found" in content:
                add_nodejs_to_dockerfile(selected_dockerfile)
                print("Detected issue with npm. Added Node.js and npm installation to Dockerfile.")
                response = os.system(f"docker build -t {image_name} -f {selected_dockerfile} {dockerfile_directory}")
                
    if response == 0:
        print(f"{selected_dockerfile} has been built as {image_name}!\n")
    else:
        print("Failed to build Docker image. Check the Dockerfile and try again.")




def add_nodejs_to_dockerfile(dockerfile_path):
    with open(dockerfile_path, 'r') as f:
        content = f.readlines()

    # Insert Node.js installation commands after the 'FROM' statement
    for index, line in enumerate(content):
        if line.startswith('FROM'):
            break
    else:
        index = -1

    node_install_cmds = [
        '\n',
        '# Installing Node.js and npm\n',
        'RUN apt-get update && apt-get install -y curl\n',
        'RUN curl -fsSL https://deb.nodesource.com/setup_16.x | bash -\n',
        'RUN apt-get install -y nodejs\n',
        '\n'
    ]
    
    content[index+1:index+1] = node_install_cmds

    with open(dockerfile_path, 'w') as f:
        f.writelines(content)

