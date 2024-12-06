#!/bin/bash
set -e
set -x

# Directory where output files go
OUTDIR=ag4mout
# Directory containing AG4Masses source files
AG4MDIR=ag4masses
# Directory containing external libraries including ag_ckpt_vocab and meliad
AGLIB=aglib
AGDIR=$AG4MDIR/alphageometry
export PYTHONPATH=$PYTHONPATH:$AGDIR:$AGLIB

# stdout, solution is written here
OUTFILE=$OUTDIR/solution.out
# stderr, a lot of information, error message, log etc.
ERRFILE=$OUTDIR/ag.err

# stdout and stderr are written to both ERRFILF and console
exec > >(tee $ERRFILE) 2>&1

# BATCH_SIZE: number of outputs for each LM query
# BEAM_SIZE: size of the breadth-first search queue
# DEPTH: search depth (number of auxilary points to add)
# NWORKERS: number of parallel run worker processes. Rule of thumb: on a 128G machine with 16 logical CPUs,
#   use NWORKERS=8, BATCH_SIZE=24.
# 
# Memory usage is affected by BATCH_SIZE, NWORKER and complexity of the problem.
# Larger NWORKER and BATCH_SIZE tends to cause out of memory issue

BATCH_SIZE=32
BEAM_SIZE=512
DEPTH=16
NWORKERS=1

#The results in Google's paper can be obtained by setting BATCH_SIZE=32, BEAM_SIZE=512, DEPTH=16

PROB_FILE=$OUTDIR/output.txt
PROB=Output
# alphageometry | ddar
MODEL=ddar
DATA=$AGLIB/ag_ckpt_vocab
MELIAD_PATH=$AGLIB/meliad
export PYTHONPATH=$PYTHONPATH:$MELIAD_PATH

DDAR_ARGS=(
  --defs_file=$AGDIR/defs.txt \
  --rules_file=$AGDIR/rules.txt \
);

SEARCH_ARGS=(
  --beam_size=$BEAM_SIZE
  --search_depth=$DEPTH
)

LM_ARGS=(
  --ckpt_path=$DATA \
  --vocab_path=$DATA/geometry.757.model \
  --gin_search_paths=$MELIAD_PATH/transformer/configs,$AGDIR \
  --gin_file=base_htrans.gin \
  --gin_file=size/medium_150M.gin \
  --gin_file=options/positions_t5.gin \
  --gin_file=options/lr_cosine_decay.gin \
  --gin_file=options/seq_1024_nocache.gin \
  --gin_file=geometry_150M_generate.gin \
  --gin_param=DecoderOnlyLanguageModelGenerate.output_token_losses=True \
  --gin_param=TransformerTaskConfig.batch_size=$BATCH_SIZE \
  --gin_param=TransformerTaskConfig.sequence_length=128 \
  --gin_param=Trainer.restore_state_variables=False
);

true "=========================================="

python -m alphageometry \
--alsologtostderr \
--problems_file=$PROB_FILE \
--problem_name=$PROB \
--mode=$MODEL \
"${DDAR_ARGS[@]}" \
"${SEARCH_ARGS[@]}" \
"${LM_ARGS[@]}" \
--out_file=$OUTFILE \
--n_workers=$NWORKERS 2>&1
