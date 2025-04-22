import argparse
from tqdm import tqdm
from vllm import LLM, SamplingParams
from openai import OpenAI
import pandas as pd
from prompt import prompt_dict

def chat(llm, user_message):
    messages = [
        {"role": "user", "content": user_message}
    ]

    output = llm.chat(messages, sampling_params=sampling_params, use_tqdm=False)
    return output[0].outputs[0].text


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
                    if "EN" in args.task_id:
                        response = chat(llm, row["instruction"] + "Let's think step by step.\n\n")
                    else:
                        response = chat(llm, row["instruction"] + "请一步一步思考。\n\n")
                else:
                    if "EN" in args.task_id:
                        response = chat(llm, instruction + "\n" + row["instruction"] + "Let's think step by step.\n\n")
                    else:
                        response = chat(llm, instruction + "\n" + row["instruction"] + "请一步一步思考。\n\n")
            except Exception as e:
                continue
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

    parser.add_argument('--model_path', required=True, type=str)
    parser.add_argument('--task_id', required=True, help="x-x-EN/CH", type=str)
    parser.add_argument('--data_path', type=str)
    parser.add_argument('--output_path', type=str)
    args = parser.parse_args()

    if args.task_id == "3-5-EN" or "4-1" in args.task_id or "4-2" in args.task_id:
        sampling_params = SamplingParams(temperature=0.0, max_tokens=16384)
    else:
        sampling_params = SamplingParams(temperature=0.0, max_tokens=8192)
    llm = LLM(model=args.model_path, gpu_memory_utilization=0.75)

    print(f"[INFO]====== Task: {args.task_id} CoT======")
    print(f"[INFO]====== Model: {args.model_path} ======")

    instruction = prompt_dict[args.task_id]

    df = pd.read_json(args.data_path, lines=True)

    inference(instruction, df, args.output_path)
