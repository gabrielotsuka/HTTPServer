# HTTPServer
Project meant to study more about HTTP servers and Python with Tornado framework. This POC downloads a file from the server to the client.
This description will be followed by the steps to install the requirements to run the project in Ubuntu OS.

# Requirements
- Python: The language used in this project is Python. The version installed will be 3.8 because Tornado framework requires Python version 3.5.2 or above. 
    ```
    sudo sudo apt update
    sudo apt install software-properties-common
    sudo add-apt-repository ppa:deadsnakes/ppa
    sudo apt install python3.8
    ```

    To ensure that Python was correctly installed, run:
    ```
    python3 --version
    ```
    The output should be like this:
    ```
    Python 3.8.10
    ```
<br />

- Python pip: Used as the standard package manager for Python, it is an requirement to download the Tornado Framework
    ```
    sudo apt install python3-pip
    ```
<br />

- Tornado: Tornado framework is a web framework and asynchronous networking library. To install it, run the command:
    ```
    pip install tornado
    ```

# Usage
To start the application, run the following command from inside the HTTPServer directory:
```
python3 FileDownloader.py
```
It will start the server, and the application will be running on port 8080. 
You should insert the file in the HTTPServer directory, and to the client download it, he must access this uri, changing the file_name to the name of the file with its extension.
```
localhost:8080/<file_name>
```
Obs: The file name shall not have spaces nor accented characters.

If you don't want to put any other files in the repository, you can give it a try by downloading this README file!
```
localhost:8080/README.md
```