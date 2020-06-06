# transform-2020-tutorial

**_Idea to MVP_ tutorial at TRANSFORM 2020**

----

# NOT YET FINAL

You are welcome to look around, but you may have to update or re-download when we release the final version (about 10 June).

----

This repo contains everything you need to follow along with the tutorial. You can clone it with `git` or use the green button to download a ZIP file. Put it where you would normally keep your project files.

I'll assume you have the `conda` package and environment manager. (If you don't have it, you can install it [from here](https://docs.conda.io/en/latest/miniconda.html).)


## Create an environment

    conda env create -f environment.yml
    conda activate t20-fri-mvp
    python -m ipykernel install --user --name t20-fri-mvp

Now you're ready to use the notebooks and the app in this repo.


## Agenda

- Introduction to this problem
- `notebooks/Fossil_classifier_minimal.ipynb`
- `notebooks/Hitting_some_web_APIs.ipynb`
- `notebooks/Building_a_flask_app.ipynb` (note that this is not a 'normal' notebook)
- `notebooks/Hitting_our_web_API.ipynb`

We will build everything else from scratch. However, there are 'complete' notebooks in `nb-master` if you prefer to read rather than type. And there is a complete app in `app-master` if you want the complete app.
