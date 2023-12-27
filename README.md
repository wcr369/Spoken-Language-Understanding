<h1 align="center">
Exploring Spoken Language Understanding
</h1>
<p align="center">
    Project of CS3602 Natural Language Processing, 2023 Fall, SJTU
    <br />
    <a href="https://github.com/wcr369"><strong>Chenrun Wang</strong></a>
    &nbsp;
    <a href="https://github.com/xxyQwQ"><strong>Xiangyuan Xue</strong></a>
    &nbsp;
    <a href="https://github.com/Ken-Bing"><strong>Zeyi Zheng</strong></a>
    <br />
</p>
<p align="center">
    <a href='https://github.com/wcr369/Spoken-Language-Understanding'> <img alt='Project Report' src='https://img.shields.io/badge/Project-Report-green?style=flat&logo=googlescholar&logoColor=green'> </a>
    <a href="https://github.com/wcr369/Spoken-Language-Understanding"> <img alt="Github Repository" src="https://img.shields.io/badge/Github-Repository-blue?logo=github&logoColor=blue"> </a>
</p>

This project aims to explore different algorithms for spoken language understanding.

## 🛠️ Requirements

To ensure the code runs correctly, following packages are required:

* `python`
* `pytorch`

You can install them following the instructions below.

* Create a new conda environment and activate it:
  
    ```bash
    conda create -n pytorch python=3.10
    conda activate pytorch
    ```

* Install [pytorch](https://pytorch.org/get-started/previous-versions/) with appropriate CUDA version, e.g.
  
    ```bash
    pip install torch==1.12.1+cu113 torchvision==0.13.1+cu113 torchaudio==0.12.1 --extra-index-url https://download.pytorch.org/whl/cu113
    ```

Latest version is recommended for all the packages, but make sure that your CUDA version is compatible with your `pytorch`.

## 🚀 Experiments

### SLU Tagging

This is a baseline model based on recurrent neural network. Run the following command to train the model:

```bash
python -X utf8 main.py --model slu_tagging --device 0
```

Run the following command to test the model:

```bash
python -X utf8 main.py --model slu_tagging --testing --testing_path ./path/to/your/model/weights
```

### SLU Bert

This model utilizes a pretrained BERT model as the backbone. The learning rate should be relatively small for finetuning. Run the following command to train the model:

```bash
python -X utf8 main.py --model slu_bert --device 0 --lr 5e-5
```

Run the following command to test the model:

```bash
python -X utf8 main.py --model slu_bert --testing --testing_path ./path/to/your/model/weights
```
