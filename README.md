# Laroza Movies & Series Extractor

This script allows you to extract movies and series links from the Laroza website.

## Usage

### Prerequisites
- Install **Python 3.12 or above**
- Clone the repository using the command:
  ```sh
  git clone https://github.com/sheerien/laroza.git
  ```
- Navigate to the project directory:
  ```sh
  cd <repository-folder>
  ```

### Setup Virtual Environment
#### Windows
```sh
python -m venv venv
venv\Scripts\activate
```
#### Linux & Mac
```sh
python3 -m venv venv
source venv/bin/activate
```

### Install Dependencies
Once the virtual environment is activated, install the required libraries:
```sh
pip install -r requirements.txt
```

### Configure the `.env` File
- Copy the existing `.inf` example file and paste it as `Series.inf`:
  ```sh
  cp .env.example ..env
  ```
- Modify `.env` with your desired configurations.

### Run the Script
#### Windows
```sh
py script.py Series.inf
```
#### Mac & Linux
```sh
python3 script.py Series.inf
```

## Notes
- Ensure all required dependencies are installed before running the script.
- Always activate the virtual environment before executing the script.
- The `.inf` file contains the necessary configurations for extracting links.

## Ramadan 2025 Category
For extracting Ramadan 2025 content, visit:
[Larosa Ramadan 2025](https://w.laroza.now/category.php?cat=ramadan-2025)

### License
This project is open-source. Feel free to modify and contribute!

