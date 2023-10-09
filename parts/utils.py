import os
from .docker_utils import *

def main_menu():
    while True:
        print("Script Manager")
        print("1. Docker")
        print("2. Quit")
        choice = input("Enter your choice: ")

        if choice == '1':
            docker_menu()
        elif choice == '2':
            exit()
        else:
            print("Invalid choice!")

def docker_menu():
    while True:
        print("\nDocker Options")
        print("1. Initialize Docker Project")
        print("2. Check and Install Docker (Ubuntu)")
        print("3. Search Docker Images")
        print("4. List Docker Images")
        print("5. Delete Docker Image")
        print("6. Modify Dockerfile")
        print("7. Back to main menu")
        print("8. List Docker Containers")
        print("9. Delete Docker Container")
        print("10. Build Docker Image from Dockerfile") # New option
        choice = input("Enter your choice: ")

        if choice == '1':
            initialize_docker_project()
        elif choice == '2':
            check_and_install_docker()
        elif choice == '3':
            search_docker_images()
        elif choice == '4':
            list_docker_images()
        elif choice == '5':
            delete_docker_image()
        elif choice == '6':
            modify_dockerfile()
        elif choice == '7':
            return
        elif choice == '8':
            list_docker_containers()
        elif choice == '9':
            delete_docker_container()
        
        elif choice == '10':
            build_docker_image()

        else:
            print("Invalid choice!")

        input("\nPress any key to continue...")
