from reader import Reader
from utils import *
import argparse

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Generate Geometry Answer')
    parser.add_argument('--model', type=str, default='gemma2-9b-it', help='Model to use for generation', choices=['gpt-4o-mini', 'gemma2-9b-it'])
    parser.add_argument('--question', type=str, required=True, help='Question to generate answer for')
    args = parser.parse_args()
    if args.model == 'gpt-4o-mini':
        get_github_token()
    elif args.model == 'gemma2-9b-it':
        get_grog_api()
    reader = Reader(model=args.model)
    input = translate(args.question)
    reader.main(input)
    run_ag()