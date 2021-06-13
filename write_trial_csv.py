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
mocap_data = [txt for txt in glob("bvh/mocap/newMocapBVHs/*.txt") if "attention-check" not in txt]
attention_check_data = [txt for txt in glob("bvh/mocap/newMocapBVHs/*.txt") if "attention-check" in txt]
orders = ['mocap_left', 'model_left']
trial_list = []
attention_check_list = []
for order in orders:
    for mocap in mocap_data:
        mocap_number = mocap.replace(".txt", "").replace("bvh/mocap/newMocapBVHs/clip", "")
        for model in model_data:
            print("modelnumberNOrmal " + model[-18])
            if model[-18] == mocap_number:
                trial_list.append((model, mocap, order))
        for attention_check in attention_check_data:
            attention_check_list.append((attention_check, mocap, order))
                #trial_list = [(model, mocap, order) for model, mocap, order in it.product(model_data, mocap_data, orders)
 #             if model[-2] == mocap.replace(".txt", "").replace("clip", "")]
#attention_check_list = [(attention_check, mocap, order) for attention_check, mocap, order in it.product(attention_check_data, mocap_data, orders)
 #                       if attention_check[-2] == mocap.replace(".txt", "").replace("clip-attention-check", "")]


s = ''
for model, mocap, order in trial_list:
    s+= model + ';'
    s+= mocap + ';'
    s+= order + '\n'
print('write new_trials.csv')
with open('new_trials.csv', 'w') as fo:
    fo.write(s)

s = ''
for attention_check, mocap, order in attention_check_list:
    s+= attention_check + ';'
    s+= mocap + ';'
    s+= order + '\n'
print('write new_attention_check_trials.csv')
with open('new_attention_check_trials.csv', 'w') as fo:
    fo.write(s)
