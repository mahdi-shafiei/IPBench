import argparse
from tqdm import tqdm
from openai import OpenAI
import pandas as pd
from prompt import prompt_dict

import httpx

client = OpenAI(
    base_url="",
    api_key="",
    http_client=httpx.Client(
        base_url="",
        follow_redirects=True,
    ),
)

def chat(model_name, user_message):
    if args.task_id == "3-5-EN" or "4-1" in args.task_id or "4-2" in args.task_id:
        max_tokens = 16384
    else:
        max_tokens = 8192
    completion = client.chat.completions.create(
        model=model_name,
        messages=[
            {"role": "user", "content": user_message}
        ],
        temperature=0.0,
        max_tokens=max_tokens,
    )
    return completion.choices[0].message.content


def inference(instruction, df, output_path):
    df_iter = tqdm(df.iterrows(), total=len(df))
    results = []
    instructions = []
    labels = []
    for index, row in df_iter:
        response = None
        while response is None:
            try:
                if instruction == "":
                    response = chat(args.model_name, row["instruction"])
                else:
                    response = chat(args.model_name, instruction + "\n" + row["instruction"])
            except Exception as e:
                print(e)
                continue
        # print(response)
        results.append(response)
        instructions.append(row["instruction"])
        labels.append(row["output"])

    re_df = pd.DataFrame.from_records({
        "instruction": instructions,
        "response": results,
        "label": labels
    })
    re_df.to_json(output_path, orient="records", force_ascii=False)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument('--model_name', required=True, type=str)
    parser.add_argument('--task_id', required=True, help="x-x-EN/CH", type=str)
    parser.add_argument('--data_path', type=str)
    parser.add_argument('--output_path', type=str)
    args = parser.parse_args()

    print(f"[INFO]====== Task: {args.task_id} ======")
    print(f"[INFO]====== Model: {args.model_name} ======")

    instruction = prompt_dict[args.task_id]

    df = pd.read_json(args.data_path, lines=True)

    inference(instruction, df, args.output_path)
