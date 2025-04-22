CUDA_VISIBLE_DEVICES=gpu_rank python inference-fewshot.py \
--task_id rask_id \
--k k \
--model_path model_path \
--data_path data_path \
--output_path output_path
