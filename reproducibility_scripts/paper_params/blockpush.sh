# To train.

python train.py \
  env=blockpush \
  experiment.num_cv_runs=5 \
  experiment.save_subdir=reproduction/paper_params

# To evaluate.

python run_on_env.py \
  env=blockpush \
  model.load_dir="$(pwd)"/train_runs/train_blockpush/reproduction/paper_params/0 \
  experiment.save_subdir=reproduction/paper_params/0 \
  experiment.vectorized_env=True \
  experiment.async_envs=True \
  experiment.num_envs=20 \
  experiment.num_eval_eps=50 \
  experiment.device=cpu

# To compute metrics.

python compute_metrics.py \
  load_dir="$(pwd)"/eval_runs/eval_blockpush/reproduction/paper_params/0/ \
  tags=\'best,paper,compute_metrics\' \
  save_subdir=blockpush/reproduction/paper_params/0