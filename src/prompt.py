MCQA_EN = "Please answer the following question thoughtfully and provide your final answer at the end in the format 'Answer: **option**'\n\nQuestion:\n\n"
MCQA_CH = "请认真回答以下问题，并在最后按照格式'Answer: **选项**'来提供你的最终答案。\n\n问题：\n\n"

prompt_1_5_1_EN = "Please answer the following question thoughtfully and provide your final answer at the end in the format 'Answer: **corresponding IPC number**'\n\nQuestion:\n\n"
prompt_1_5_1_CH = "请认真回答以下问题，并在最后按照格式'Answer: **对应的IPC号**'来提供你的最终答案。\n\n问题：\n\n"

prompt_1_5_2_EN = "Please answer the following question thoughtfully and provide your final answer at the end in the format 'Answer: **corresponding CPC number**'\n\nQuestion:\n\n"

prompt_3_5_EN = "Please examine the patents in # Patent Applications Awaiting Examination. Determine whether each patent application should be allowed or rejected.\n\nReturn your decision in the following format:\n\nAnswer: allowed / rejected\n\n"

prompt_4_1_EN = ""
prompt_4_1_CH = ""

prompt_dict = {
    "1-1-EN": MCQA_EN,
    "1-1-CH": MCQA_CH,

    "1-2-EN": MCQA_EN,
    "1-2-CH": MCQA_CH,

    "1-3-EN": MCQA_EN,
    "1-3-CH": MCQA_CH,

    "1-4-EN": MCQA_EN,
    "1-4-CH": MCQA_CH,

    "1-5-1-EN": prompt_1_5_1_EN,
    "1-5-1-CH": prompt_1_5_1_CH,

    "1-5-2-EN": prompt_1_5_2_EN,

    "1-6-EN": MCQA_EN,
    "1-6-CH": MCQA_CH,

    "1-7-EN": MCQA_EN,
    "1-7-CH": MCQA_CH,

    "2-1-EN": MCQA_EN,
    "2-1-CH": MCQA_CH,

    "2-2-EN": MCQA_EN,
    "2-2-CH": MCQA_CH,

    "2-5-CH": MCQA_CH,

    "2-3-EN": MCQA_EN,
    "2-3-CH": MCQA_CH,

    "2-4-EN": MCQA_EN,
    "2-4-CH": MCQA_CH,

    "3-1-EN": MCQA_EN,
    "3-1-CH": MCQA_CH,

    "3-2-EN": MCQA_EN,
    "3-2-CH": MCQA_CH,

    "3-3-EN": MCQA_EN,
    "3-3-CH": MCQA_CH,

    "3-4-EN": MCQA_EN,
    "3-4-CH": MCQA_CH,

    "3-5-EN": prompt_3_5_EN,

    "4-1-EN": prompt_4_1_EN,
    "4-1-CH": prompt_4_1_CH,

    "4-2-EN": prompt_4_1_EN,
    "4-2-CH": prompt_4_1_CH,

    "4-3-EN": MCQA_EN,
    "4-3-CH": MCQA_CH,
}
