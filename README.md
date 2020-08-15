Download game archives from KGS.

## Installation

You need to have python3 and pip3 installed.
Python 3.8.3 works. Lower python 3 versions may work but have not been tested.

Clone the repository.

```
git clone https://github.com/Sven-C/go-archiver.git
cd go-archiver
```

Create a virtual python environment.

Using venv:
```
python -m venv env
source env/bin/activate
```

Using virtualenv:
```
pip3 intstall virtualenv
virtualenv env
source env/bin/activate
```

Install the requirements.

```
pip3 install -r requirements.txt
```

Execute the script.

```
./src/kgs-archiver.py <kgsnickname>
```
