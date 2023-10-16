# Train with params in the paper.

python train.py \
  env=kitchen \
  experiment.num_cv_runs=3 \
  model=mlp \
  experiment.save_subdir=reproduction/ablation_mlp/paper

# Eval with params in the paper.

python run_on_env.py \
  env=kitchen \
  model.load_dir="$(pwd)"/train_runs/train_kitchen/reproduction/ablation_mlp/paper/0 \
  experiment.save_subdir=reproduction/ablation_mlp/paper/0 \
  experiment.vectorized_env=True \
  experiment.async_envs=True \
  experiment.num_envs=20 \
  experiment.num_eval_eps=50 \
  experiment.device=cpu

# To compute metrics.

python compute_metrics.py \
  load_dir="$(pwd)"/eval_runs/eval_kitchen/reproduction/ablation_mlp/paper/0 \
  tags=\'ablation,mlp,paper,compute_metrics\' \
  save_subdir=kitchen/reproduction/ablation_mlp/paper/0

# Train with best sweep params.
## Best one was:
## train_runs/train_kitchen/reproduction/ablation_mlp_sweep/20
## Retrain with 3 seeds.

python train.py \
  env=kitchen \
  experiment.num_cv_runs=3 \
  model=mlp \
  experiment.lr=0.00053 \
  experiment.grad_norm_clip=inf \
  experiment.weight_decay=0.01 \
  model.hidden_dim=120 \
  model.hidden_depth=6 \
  model.batchnorm=True \
  experiment.save_subdir=reproduction/ablation_mlp/sweep_best

# Eval with best sweep params.

python run_on_env.py \
  env=kitchen \
  model.load_dir="$(pwd)"/train_runs/train_kitchen/reproduction/ablation_mlp/sweep_best/0 \
  experiment.save_subdir=/reproduction/ablation_mlp/sweep_best/0 \
  experiment.vectorized_env=True \
  experiment.async_envs=True \
  experiment.num_envs=20 \
  experiment.num_eval_eps=50 \
  experiment.device=cpu

# To compute metrics.

python compute_metrics.py \
  load_dir="$(pwd)"/eval_runs/eval_kitchen/reproduction/ablation_mlp/sweep_best/0 \
  tags=\'ablation,mlp,sweep_best,compute_metrics\' \
  save_subdir=kitchen/reproduction/ablation_mlp/sweep_best/0

