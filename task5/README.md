# [NLP] Morphosyntactic tagging

Task for Natural Language Processing course, focusing on morphosyntactic tagging.

[Task description](./5-tagging.md)

[Task results](./results.md)

## Running
* Download Docker image:
  `sudo docker pull djstrong/krnnt2`
* Run Docker container:
  `sudo docker run -it -p 9200:9200 djstrong/krnnt2 python3 /home/krnnt/krnnt/krnnt_serve.py /home/krnnt/krnnt/data`
* Run `runall.sh`. Results will be generated as `results.md` and displayed on the screen...
* ...or run `main.py`. Results will be displayed on the screen and saved in `results.txt`.

## Requirements
* Docker (tested with 18.09.2)
* Python library `requests` as specified in `requirements.txt`
* I assume input files in a directory `ustawy` in the root directory of a repository
* Tested with Python 3.6.7