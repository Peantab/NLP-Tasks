# Results

## SVM with TF-IDF
* full text:
    * Precision: 0.91
    * Recall: 0.95
    * F1-Score: 0.93
* 10 percent
    * Precision: 0.82
    * Recall: 0.76
    * F1-Score: 0.79
* 10 lines:
    * Precision: 0.79
    * Recall: 0.94
    * F1-Score: 0.86
* 1 line:
    * Precision: 0.64
    * Recall: 0.79
    * F1-Score: 0.71

## fastText
e.g.: `./fasttext test-label ../fasttext_one_line.bin ../data/one_line_tes.csv 1 0.51`

* full text:
    * Precision: 0.925170
    * Recall: 0.978417
    * F1-Score: 0.951049
* 10 percent:
    * Precision: 0.626263
    * Recall: 0.892086
    * F1-Score: 0.735905
* 10 lines:
    * Precision: 0.834437
    * Recall: 0.919708
    * F1-Score: 0.875000
* 1 line:
    * Precision: 0.626316
    * Recall: 0.862319
    * F1-Score: 0.725610

## Flair

* full text would take ages...
* 10 percent - work in progress...
* 10 lines:
    * Precision: 0.7500
    * Recall: 0.7883
    * F1-Score: 0.7687
* 1 line:
    * Precision: 0.5955
    * Recall: 0.9493
    * F1-Score: 0.7319