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

    option_str = ''.join([chr(65 + i) for i in range(len(options))]) if options else 'ABCD'

    patterns = [
        f'(?i)(?:Final\s+answer|Answer|最终答案)[\s]*:?[\s\n]*?' 
        f'(?:[\*\$\\{{(\[\\\\(]*?(?:(?:\\\\boxed|\\\\mathbf|\\\\mathrm|\\\\text){{)?)*'
        f'(\*\*?[{option_str}]\*\*?|[{option_str}])' 
        f'(?:\\\\?\}}?\$?\)?\]?\}}?)*(?:[\s:\.\*)]|$)',
    ]

    for pattern in patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            return match.group(1).strip("**")

    return "error"

def score(file_name,output):
    df = pd.read_json(file_name)
    instructions = []
    answers = []
    model_answers = []
    scores = []
    count = 0
    df_iter = tqdm(df.iterrows(), total=len(df))
    for index, row in df_iter:
        answer = row["label"]
        model_output = extract_option_labels(row["response"], options='ABCD')
        if model_output.strip() == answer:
            count += 1
            scores.append(1)
            model_answers.append(model_output)
        elif model_output == 'error':
            scores.append("error")
            model_answers.append(row["response"])
        else:
            scores.append(0)
            model_answers.append(model_output)
        answers.append(answer)
        instructions.append(row["instruction"])
        df_iter.set_description(f"score: {count/len(df):.4f}")
    new_df = pd.DataFrame({
        "instruction": instructions,
        "response": model_answers,
        "label": answers,
        "score": scores
    })
    new_df.to_excel(output)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument('--file_name', required=True, type=str)
    parser.add_argument('--output', required=True, type=str)
    args = parser.parse_args()

    score(args.file_name,args.output)
