# MBTA Challenge

This Python application allows you to interact with the MBTA transit system through the command line. It provides functionality to list subway routes, find the longest and shortest routes, and find viable paths between two subway stops.

## Requirements

* You do not need an MBTA api key, but you may get rate limited without one. Set a variable named ``MBTA_API_KEY`` in a ``.secrets.env`` file in the root of this repo and it will be used.

* You can install the necessary dependencies using:

### Using ``uv``
I managed this project using [uv](https://docs.astral.sh/uv/). If using uv, you can just sub ``uv run`` for ``python`` for the below commands and it will ensure the program runs in a
properly configured environment.

### Not using ``uv``
* Required an environment of python 3.10+. You can use the generated ``requirements.txt`` and then run the program like show below.

```bash
pip install -r requirements.txt
```

## Usage
In a terminal session in the ``src`` directory, you can run the application by using the following syntax:

```bash
python main.py [COMMAND] [ARGS]
```

### Commands
The available commands and their usage are as follows:

**question-1**: Returns a list of all subway routes with their "long names". This command does not take any additional args.

```bash
python main.py question-1
```

**question-2**:
Returns the longest and shortest subway routes along with a list of stops that are used by multiple routes. This command does not take any additional args.

```bash
python main.py question-2
```

**find-path**
Find a viable path of subway routes between two stops. This command requires the ``--start`` and ``--end`` args, which specify the names of the starting and ending subway stops.

Example usage:
```bash
python main.py find-path --start "Forest Hills" --end "Mattapan"
```

### Help
To see more information on usage, just use the help flag ``-h``/``--help`` e.g. 
```bash
python main.py --help
```
or to see information about a specific command
```bash
python main.py [COMMAND] --help
```

### Notes
Overall:
* Since this is a stateless CLI program, each invocation must refetch and transform data that could have been precomputed and cached/stored for efficiency.

Question 2:
* For the longest and shortest subway routes, if there are two routes of the same length tied for most/last, it will just return the one it sees first, not multiple.
* My initial implementation of question 2 was slightly more efficient than my final one. I traded off efficiency of looping through the data once to get all three answers for 1. separating the functions for better testability and 2. code re-use with part of the path-finding solution for question 3 (both use the get_subway_stop_to_routes_mapping).  