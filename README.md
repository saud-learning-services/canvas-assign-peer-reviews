# Canvas Nesting Doll Peer Reviews

> - name: canvas-nesting-doll-peer-reviews
> - ops-run-with: jupyter
> - python>=3.7
> - canvasapi>=2.0.0
> - supports universal environment 🌎

⛔️ WIP ⛔️

## Summary

This project is currently designed for a specific case at Sauder - to assign "Nesting Doll Peer Reviews". Peer reviews are extracted from the first assignment entered, and new peer reviews are assigned to the second assignment entered. The assumption is that the second assignment involves the students providing feedback on the original peer reviews. 

## Input

- Canvas Course ID
- Assignment ID to extract original peer reviews from
- Assignment ID to assign new peer reviews to
  
## Output

## Important Caveats

- running this overwrites existing peer reviews for the assignment where peer reviews are assigned
- this assumes the assignment where peer reviews are assigned has no submission, when you run the autosubmit it will overwrite any existings submissions
- the assignment where peer reviews are assigned should be a text entry submission type
- you cannot undo!

## Getting Started

### Sauder Operations

_Are you Sauder Operations Staff? Please go [here](https://github.com/saud-learning-services/instructions-and-other-templates/blob/main/docs/running-instructions.md) for detailed instructions to run in Jupyter. ("The Project", or "the-project" is "canvas-nesting-doll-peer-reviews" or "Canvas Nesting Doll Peer Reviews")._

> Project uses **conda** to manage environment (See official **conda** documentation [here](https://docs.conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html#creating-an-environment-from-an-environment-yml-file))

> You will also need to create a .env file! Instructions below 


#### First Time

1. Ensure you have [conda](https://docs.conda.io/projects/conda/en/latest/user-guide/install/index.html) installed (Python 3.9 version) or [miniconda](https://docs.conda.io/en/latest/miniconda.html)
> we recommend miniconda if you don't need the Anaconda GUI
2. Clone **canvas-nesting-doll-peer-reviews** repository
3. Import environment (once): `$ conda env create -f environment.yml`
4. Create .env file aned include:

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
   1. navigate to your directory `$ cd YOUR_PATH/canvas-nesting-doll-peer-reviews`
   1. in terminal activate the environment (see step 3 on first run) `$ conda activate canvas-nesting-doll-peer-reviews` (also works with 🌎 canvas-universal-env)
   2. ensure you have a .env file in the project folder with active token information
   3. in the terminal launch a jupyter notebook `$ jupyter notebook`
   4. open appropriate jupyter notebook and follow instructions 

