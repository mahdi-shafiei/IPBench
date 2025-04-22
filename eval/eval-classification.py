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

import re

def extract_option_labels(text, options='ABCD'):
    if not isinstance(text, str) or not isinstance(options, str):
        return "error"

    patterns = [
        r'(?i)\*\*\s*Final\s+Answer\s*\*\*:?[\s\n]*\*\*?([A-H]\d{2}[A-Z]?\s?\d+/\d+)\*?',

        r'(?i)Final\s+Answer:?[\s\n]*([A-H]\d{2}[A-Z]?\s?\d+/\d+)',

        r'(?i)Answer:?[\s\n]*\*\*?([A-H]\d{2}[A-Z]?\s?\d+/\d+)\*?',

        r'(?i)最终答案:?[\s\n]*([A-H]\d{2}[A-Z]?\s?\d+/\d+)',

        r'(?i)(?:\\textbf{|\\mathbf{|\\mathrm{|\\text{)?([A-H]\d{2}[A-Z]?\s?\d+/\d+)}?'
    ]

    for pattern in patterns:
        match = re.search(pattern, text, re.IGNORECASE | re.MULTILINE)
        if match:
            return match.group(1).strip("**")

    return "error"

def score(file_name,output):
    df = pd.read_json(file_name)
    instructions = []
    answers = []
    model_answers = []
    scores = []

    section = []
    class_ = []
    subclass = []

    df_iter = tqdm(df.iterrows(), total=len(df))
    for index, row in df_iter:
        answer = row["label"]
        model_output = extract_option_labels(row["response"], options='ABCD')
        model_output = model_output.replace(" ", "")
        if model_output.strip() != "error" and model_output != "" and model_output is not None:
            if model_output.strip()[0] == answer[0]:
                section.append(1)
            else:
                section.append(0)
            if model_output.strip()[0:3] == answer[0:3]:
                class_.append(1)
            else:
                class_.append(0)
            if model_output.strip()[0:4] == answer[0:4]:
                subclass.append(1)
            else:
                subclass.append(0)
            if model_output.strip() == answer:
                scores.append(1)
            else:
                scores.append(0)
            model_answers.append(model_output)
        elif model_output == 'error':
            scores.append("error")
            section.append("error")
            class_.append("error")
            subclass.append("error")
            model_answers.append(row["response"])
        else:
            scores.append(0)
            section.append(0)
            class_.append(0)
            subclass.append(0)
            model_answers.append(model_output)
        answers.append(answer)
        instructions.append(row["instruction"])
        df_iter.set_description(f"score: {len(list(filter(lambda x: x == 1, scores)))/len(df):.4f}, section: {len(list(filter(lambda x: x == 1, section)))/len(df):.4f}, class: {len(list(filter(lambda x: x == 1, class_)))/len(df):.4f}, subclass: {len(list(filter(lambda x: x == 1, subclass)))/len(df):.4f}")
    new_df = pd.DataFrame({
        "instruction": instructions,
        "response": model_answers,
        "label": answers,
        "score": scores,
        "section": section,
        "class": class_,
        "subclass": subclass,
    })
    new_df.to_excel(output)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument('--file_name', required=True, type=str)
    parser.add_argument('--output', required=True, type=str)
    args = parser.parse_args()

    score(args.file_name,args.output)
