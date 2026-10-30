# Titanic trainer

`train_titanic.py` trains a small survival classifier (CUDA via torch if a GPU is present, otherwise scikit-learn on CPU).
Used by the MLTorq Titanic pipeline: clone this repo -> load CSV -> train -> evaluate -> gate -> register.

Dataset: not copied here, because the common public copies state no license. The pipeline downloads it at run time from
https://raw.githubusercontent.com/datasciencedojo/datasets/master/titanic.csv (origin: the public Kaggle / Encyclopedia Titanica passenger list).
Synthetic fallback data is turned off in the pipeline, so a failed download fails the run visibly.
