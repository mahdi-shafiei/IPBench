import argparse
from tqdm import tqdm
from vllm import LLM, SamplingParams
from openai import OpenAI
import pandas as pd
from prompt import prompt_dict

seed = 42

def chat(llm, user_message):
    messages = [
        {"role": "user", "content": user_message}
    ]

    output = llm.chat(messages, sampling_params=sampling_params, use_tqdm=False)
    return output[0].outputs[0].text


def inference(instruction, df, output_path, k=1):
    df_iter = tqdm(df.iterrows(), total=len(df))
    results = []
    instructions = []
    labels = []
    for index, row in df_iter:
        few_shot_df = df.sample(n=k, random_state=seed)
        few_shot_index = few_shot_df.index.tolist()
        print(index, few_shot_index)
        flag = 1
        while index in few_shot_index:
            few_shot_df = df.sample(n=k, random_state=seed+flag)
            few_shot_index = few_shot_df.index.tolist()
            flag += 1
        few_shot_prompt = f"# There are {k} examples\n\n"
        for index_, row_ in few_shot_df.iterrows():
            few_shot_prompt += f"""## Example {index_}\n\nQuestion: {row_["instruction"]}\n\nAnswer:{row_["output"]}\n\n"""
        response = None
        while response is None:
            try:
                if instruction == "":
                    response = chat(llm, few_shot_prompt + row["instruction"])
                else:
                    response = chat(llm, few_shot_prompt + instruction + "\n" + row["instruction"])
            except Exception as e:
                flag += 1
                print(e)
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
    parser.add_argument('--k', type=int)
    args = parser.parse_args()

    if args.task_id == "3-5-EN" or "4-1" in args.task_id or "4-2" in args.task_id:
        sampling_params = SamplingParams(temperature=0.0, max_tokens=32768)
    else:
        sampling_params = SamplingParams(temperature=0.0, max_tokens=8192)
    llm = LLM(model=args.model_path, gpu_memory_utilization=0.75)

    print(f"[INFO]====== Task: {args.task_id} ======")
    print(f"[INFO]====== Model: {args.model_path} ======")
    print(f"[INFO]====== k: {args.k} ======")

    instruction = prompt_dict[args.task_id]

    df = pd.read_json(args.data_path, lines=True)

    inference(instruction, df, args.output_path, k=args.k)
