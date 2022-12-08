
⛔️ WIP - DOESN'T WORK YET ⛔️

#### First Time

1. Ensure you have [conda](https://docs.conda.io/projects/conda/en/latest/user-guide/install/index.html) installed (Python 3.9 version) or [miniconda](https://docs.conda.io/en/latest/miniconda.html)
> we recommend miniconda if you don't need the Anaconda GUI
2. Clone **{PROJECT}** repository
3. Import environment (once): `$ conda env create -f environment.yml`
4. Create .env file and include:

```
API_KEY = "<your key here>"
API_URL = "https://ubc.instructure.com"
```

> Creating an env file: 
> - if you have VSCode (Mac or Windows): https://learning.oreilly.com/library/view/javascript-by-example/9781788293969/d34ba441-abb3-4937-acf1-a2e7d54ffb23.xhtmlto and enter the information into the .env file
> - Otherwise:
> 1. Open Notepad (or TextEditor) (need someting that creates plain text files)
> 2. Enter the information (API_KEY, API_URL from above) and Save
> 3. In the Save menu, set the file type to "All Files" 
> 4. Name the file .env
> 5. Hit save - you may see a warning about the file type, you want to use .env

#### Every Time

1. Run:
   1. navigate to your directory `$ cd YOUR_PATH/{PROJECT-NAME}`
   1. in terminal activate the environment (see step 3 on first run) `$ conda activate do-stuff`
   2. ensure you have a .env file in the project folder with active token information
   3. in the terminal launch a jupyter notebook `$ jupyter notebook`
   4. open appropriate jupyter notebook and follow instructions 


# Jupyter
Allow access to python files in src

```
import os
import sys
module_path = os.path.abspath(os.path.join('src/'))
if module_path not in sys.path:
    sys.path.append(module_path)
import my_app
```
