# [NLP] Morphosyntactic tagging

Task for Natural Language Processing course, focusing on morphosyntactic tagging.

[Task description](./5-tagging.md)

Task results - TBD

## Running
* Download Docker image:
  `sudo docker pull djstrong/krnnt2`
* Run Docker container:
  `sudo docker run -it -p 9200:9200 djstrong/krnnt2 python3 /home/krnnt/krnnt/krnnt_serve.py /home/krnnt/krnnt/data`

## Requirements
Docker (tested with 18.09.2)