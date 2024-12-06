# Process AG4Masses stderr output files to create cleaner log files
#
# Usage: mklog.py [-h] [-o O] [-s S] errfiles [errfiles ...]
#
# positional arguments:
#   errfiles: stderr output files of AG4Masses
#
# options:
#   -h, --help  show this help message and exit
#   -o O        Output directory. Default: .
#   -s S        Log file suffix. Default: log

import os
import re
import sys
import argparse

def aglog(errfls, outdir, logfl_suffix):
  agfiles = {
    "alphageometry.py",
    "alphageometry_test.py",
    "ar.py",
    "ar_test.py",
    "beam_search.py",
    "dd.py",
    "dd_test.py",
    "ddar.py",
    "ddar_test.py",
    #"decoder_stack.py",
    "geometry.py",
    "geometry_test.py",
    "graph.py",
    "graph_test.py",
    "graph_utils.py",
    "graph_utils_test.py",
    "lm_inference.py",
    "lm_inference_test.py",
    "models.py",
    "numericals.py",
    "numericals_test.py",
    "pretty.py",
    "problem.py",
    "problem_test.py",
    "trace_back.py",
    "trace_back_test.py"
    #"transformer_layer.py" 
    }

  for errfl_path in errfls:
    fnbase = os.path.basename(errfl_path)
    if fnbase.endswith('.err'):
      fnbase = fnbase[:-4]
    logfl_path = f'{outdir}/{fnbase}.{logfl_suffix}'

    print(f'Processing {errfl_path}, writing log to {logfl_path}')

    with open(errfl_path, 'r') as errfl:
      with open(logfl_path, 'x') as logfl:
        for line in errfl:
          m = re.search('(\S+\.py):\d+', line)
          if m and os.path.basename(m.group(1)) not in agfiles:
            #print(f'Skipping log from {m.group(1)}')
            continue
          m = re.search('\S+\.cc:\d+|jax.tree_util.register_keypaths|' +
                        'ddar\.py:.+(Depth .+ time = |Nothing added, breaking)|' +
                        '!! try_translate_constrained_to_construct|warnings.warn|'+
                        'alphageometry.py:\d+] .*(LM output|Solving:|string=)',
                        line)
          if m:
            #print('Skipping ddar log')
            continue
          logfl.write(line)

def main():
  # Create the parser
  parser = argparse.ArgumentParser(description='Process AG4Masses stderr output files to create cleaner log files')
  # Add arguments
  parser.add_argument('errfiles', nargs='+', help='stderr output files of AG4Masses')
  parser.add_argument('-o', type=str, default='.',  help='Output directory. Default: .')
  parser.add_argument('-s', type=str, default='log',  help='Log file suffix. Default: log')
  # Execute the parse_args() method
  args = parser.parse_args()

  aglog(args.errfiles, args.o, args.s)

if __name__=='__main__':
   main()
