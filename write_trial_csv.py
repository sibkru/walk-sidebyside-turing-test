from glob import glob
import os
import re
import itertools as it

inparenthesis = re.compile('\([a-zA-Z0-9\-]*\)')
beforeparenthesis = re.compile('[a-zA-Z0-9]*\(')


def parse_filename(s: str) -> dict:
    """
    Finds numbers in brackets, associates this value
    with a key in front of the bracket.
    Returns Series like {'model': 'vcgpdm',...}
    """
    A = map(remove_brackets, re.findall(inparenthesis, s))
    B = map(remove_brackets, re.findall(beforeparenthesis, s))
    return {b: a for a, b in zip(A, B)}


def remove_brackets(s):
    s = s.replace('(', '').replace(')', '')
    try:
        return int(s)
    except ValueError:
        return s


def get_model_str_from_fp(s: str) -> str:
    return s.split(os.sep)[2]


def available_condition(ds, c):
    if 'hold' in ds and c == 24:
        return False
    else:
        return True


def get_train_fn(fn, glprim):
    d = parse_filename(fn)
    ds = d['dataset']
    hold = d['hold']
    return f'bvh/{ds}-training{hold}-{glprim}.txt'

model_data = glob('bvh/generated/*/final-lines.txt')
mocap_data = [txt for txt in glob("bvh/mocap/*.txt") if "attention-check" not in txt]
attention_check_data = [txt for txt in glob("bvh/mocap/*.txt") if "attention-check" in txt]
orders = ['mocap_left', 'model_left']

trial_list = [(model, mocap, order) for model, mocap, order in it.product(model_data, mocap_data, orders) ]
attention_check_list = [(attention_check, mocap, order) for attention_check, mocap, order in it.product(attention_check_data, mocap_data, orders) ]


s = ''
for model, mocap, order in trial_list:
    s+= model + ';'
    s+= mocap + ';'
    s+= order + '\n'
print('write trials.csv')
with open('trials.csv', 'w') as fo:
    fo.write(s)

s = ''
for attention_check, mocap, order in attention_check_list:
    s+= attention_check + ';'
    s+= mocap + ';'
    s+= order + '\n'
print('write attention_check_trials.csv')
with open('attention_check_trials.csv', 'w') as fo:
    fo.write(s)
