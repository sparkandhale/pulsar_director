# Pulsar Director
A open-source tool to primarily view Apache Pulsar topic data and - secondary - control it's storage (e.g. compaction, offloading, etc.).


## How to run the application?
run the web server `uvicorn src.main:app --reload --port 8888`

### How to develop
Create the virtul environment: `py -m venv .venv`
Start the Environment: `./.venv/Scripts/activate` (or allow VS Code to start it). Use `deactivate`to stop it.

All the required libraries must be listed in requirements.txt and installed by  `python -m pip install -r .\requirements.txt`
For Dev use `python -m pip install -r .\requirements-dev.txt`

To cleanup the environment run:
`pip3 freeze > to-uninstall.txt` and then
`pip3 uninstall -y -r to-uninstall.txt`

or `pip3 install pip-autoremove`

To benefit of code-insight/completion select the venv Interpreter (Ctr) --> (Ctrl+Shift+P) then search for "Python: Select Interpreter"

## How to contribute to the application?
It is open-source, just send a pull-request and state your ideas/expectations. You can also send a pull-request to the README and describe your idea how Pulsar Director should evolve.