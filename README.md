# Theory Of Compilation
## Quick setup (shell)

```
git clone https://github.com/maciektr/compilation_lab.git
cd compilation_lab
virtualenv -p python3 venv
source venv/bin/activate
pip install -r requirements.txt
```
## Runner
You can use the parser by simply running:
```
python main.py [options]
```
There are several optional arguemnts available:
- `--path=arg`

Provides path to file that will be parsed (default is `examples/example1.m`).
- `--lexer`

Runs lexer only.
- `--clear`

Only removes output and temporary files.

- `--zip[=arg]`

Packs the program as zip (arg provides output file name).

- `--use_cache`

Uses the cache files from previous run (e.g. `parsetab.py` for `ply.yacc`).
