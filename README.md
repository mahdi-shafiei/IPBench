# IPBench
[**🌐 Homepage**](https://IPBench.github.io/) | [**🤗 Dataset**](https://huggingface.co/datasets/IPBench/IPBench) | [**🤗 Paper**]() | [**📖 arXiv**]() | [**GitHub**](https://github.com/IPBench/IPBench)


This repo contains the evaluation code for the paper "[IPBench: Benchmarking the knowledge of Large Language Models in Intellectual Property]()"
## 🔔News

## Introduction

Intellectual property, especially patents, shares similarities with academic papers in that it encapsulates the essence of domain knowledge across various technical fields. However, it is also governed by the intellectual property legal frameworks of different countries and regions. As such, it carries technical, legal, and economic significance, and is closely connected to real-world intellectual property services. In particular, intellectual property data is a rich, multi-modal data type with immense potential for content mining and analysis. Focusing on the field of intellectual property, we propose a comprehensive four-level IP task taxonomy based on the DOK model. Building on this taxonomy, we developed IPBench, a large language model benchmark consisting of 10,374 data instances across 20 tasks and covering 8 types of IP mechanisms. Compared to existing related benchmarks, IPBench features the largest data scale and the most comprehensive task coverage, spanning technical and legal tasks as well as understanding, reasoning, classification, and generation tasks.

<p align="center">
  <img src="framework.bmp" alt="introduction">
</p>

## 🏆 Mini-Leaderboard
| Open-source Models        | Score |
|---------------------------|-------|
| InstructBLIP-T5-XL        | 47.3  |
| BLIP-2 FLAN-T5-XL         | 52.8  |
| mPLUGw-OWL2               | 53.2  |
| Qwen-VL-Chat              | 53.4  |
| InstructBLIP-T5-XXL       | 56.7  |
| Mantis-8B-siglip-Llama3   | 57.5  |
| BLIP-2 FLAN-T5-XXL        | 57.8  |
| DeepSeek-VL-Chat-7B       | 60.3  |
| Yi-VL-6B-Chat             | 61.3  |
| InternLM-XComposer2-VL    | 62.1  |
| InternVL-Chat-1.5         | 66.3  |
| Idefics2-8B               | 67.7  |
| Yi-VL-34B-Chat            | 67.9  |
| MiniCPM-Llama3-2.5        | 69.4  |
| CogVLM2-Llama3-Chat       | 70.3  |
| LLaVA-1.6-34B             |**73.8**|
| **Closed-source Models**  |**Score**|
| GPT-4V                    | 65.9  |
| GPT-4o                    | 72.6  |
| Gemini-1.5 Pro            | 73.9  |
| Qwen-VL-MAX               | 74.8  |
| Claude 3.5 Sonnet         |**80.9**|



## Installation
```python
pip install -r requirements.txt
```
Specifically, if you need to run the `Yi-VL` model, please refer to the link [here](https://github.com/01-ai/Yi/blob/main/VL/README.md) to configure your environment.

## Inference
You can directly perform inference on `Yi-VL-6B` model to be tested using the following command:
```python
python infer/infer.py --model_name yi-vl-6b-chat --mode none --output_dir ./results
```

`--mode`: We provide various evaluation modes, including no additional prompts (none), keyword-based prompts (domain, emotion, rhetoric), chain-of-thought prompts (cot), and few-shot prompts (1-shot, 2-shot, 3-shot). You can use the mode parameter to select which evaluation modes to use, with the option to choose multiple modes. By default, all modes will be evaluated in a loop.

`--infer_limit`: The input for this parameter is an integer, used to limit the number of problems for this inference, aimed at saving costs while debugging API, default is unlimited.

During inference, a temporary file .jsonl.tmp will be saved. If the inference is unexpectedly interrupted, you can directly rerun the command to resume inference from the breakpoint.

After inference is complete, you can check the response field in the saved JSONL file in `output_dir`. Normally, this field should be of string type; if it is of dict type, the error field will contain error information. Rerunning the command can directly re-infer the issues that caused errors.

### Run Custom Model
`--model_name` needs to align with the filenames in the `infer/models` directory. We have some built-in models available for direct selection. 

If you add a `custom model` to be tested, you need to refer to the files in the `infer/models` directory to add a new `.py` file and add your config in [\_\_init\_\_.py](infer/models/__init__.py).


## Evaluation

After you finish inference and confirm there are no error messages, please run the answer parsing and evaluation pipeline as follows: 
```
python eval.py --model_name yi-vl-6b-chat --mode none --output_dir ./results --save_dir ./results_with_status
```
Detailed evaluation results can be found in the `save_dir`.

Alternatively, you can use the following command to evaluate the inference results of all models:
```
python eval.py --evaluate_all --output_dir ./results --save_dir ./results_with_status
```

## Contact
Qiyao Wang: wangqiyao@mail.dlut.edu.cn

Guhong Chen: 

Shiwen Ni: sw.ni@siat.ac.cn

## Citation

**BibTeX:**
```bibtex

```
