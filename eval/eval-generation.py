import json
import argparse
import os
from prettytable import PrettyTable
import pandas as pd
from openpyxl.styles import PatternFill, Font, Alignment
from tqdm import tqdm
import multiprocessing
from functools import partial
import re
from transformers import AutoTokenizer


import re
import jieba
from nltk.translate.bleu_score import sentence_bleu, SmoothingFunction
from rouge import Rouge
import bert_score

def jieba_cut(text):
    return list(jieba.cut(text))

def calculate_bleu(reference, candidate):
    smoothie = SmoothingFunction().method1 
    reference = [jieba_cut(reference)]
    candidate = jieba_cut(candidate)
    bleu_score = sentence_bleu(reference, candidate, smoothing_function=smoothie)
    return bleu_score

def calculate_rouge(reference, candidate):
    rouge = Rouge()
    reference = " ".join(jieba_cut(reference))
    candidate = " ".join(jieba_cut(candidate))
    scores = rouge.get_scores(candidate, reference)
    return scores[0] 

def calculate_bertscore(reference, candidate):
    if "en" in args.file_name:
        model_type = "allenai/longformer-base-4096"
        max_len = 4096
    elif "ch" in args.file_name:
        model_type = "ValkyriaLenneth/longformer_zh"
        max_len = 4096
    else:
        raise ValueError("Unsupported file type. Expected 'en' or 'ch' in file name.")

    tokenizer = AutoTokenizer.from_pretrained(model_type)

    def truncate(text):
        tokens = tokenizer(text, truncation=True, max_length=max_len)
        return tokenizer.decode(tokens["input_ids"], skip_special_tokens=True)

    truncated_candidate = truncate(candidate)
    truncated_reference = truncate(reference)

    P, R, F1 = bert_score.score(
        [truncated_candidate],
        [truncated_reference],
        model_type=model_type
    )

    return {
        "Precision": P.item(),
        "Recall": R.item(),
        "F1": F1.item()
    }


def score(file_name,output):
    df = pd.read_json(file_name)
    instructions = []
    answers = []
    model_answers = []
    bleus = []
    rouges = []
    bses = []
    df_iter = tqdm(df.iterrows(), total=len(df))
    for index, row in df_iter:
        answer = row["label"]
        model_output = row["response"]
        bleu = calculate_bleu(answer, model_output)
        bleus.append(bleu)
        rouge_l = calculate_rouge(answer, model_output)["rouge-l"]["f"]
        rouges.append(rouge_l)
        bs = calculate_bertscore(answer, model_output)["F1"]
        bses.append(bs)
        instructions.append(row["instruction"])
        model_answers.append(model_output)
        answers.append(answer)
        df_iter.set_description(f"avg bleu: {sum(bleus)*100/len(bleus):.4f}, avg rouge: {sum(rouges)*100/len(rouges):.4f}, avg bert-score: {sum(bses)*100/len(bses):.4f}")
    new_df = pd.DataFrame({
        "instruction": instructions,
        "response": model_answers,
        "label": answers,
        "bleu": bleus,
        "rouge": rouges,
        "bse": bses,
    })
    new_df.to_excel(output)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument('--file_name', required=True, type=str)
    parser.add_argument('--output', required=True, type=str)
    args = parser.parse_args()
    print(f"[INFO] file: {args.file_name}")

    score(args.file_name,args.output)
