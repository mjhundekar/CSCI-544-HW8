# -*- coding: utf-8 -*-
import os
import sys
import codecs
import math


def get_file_dict(paths):
    path_dict = {}
    for sub_dir in paths:
        key = sub_dir[0].split('/')[-1]
        file_names = []
        for name in sub_dir[2]:
            file_names.append(sub_dir[0] + '/' + name)
        path_dict[key] = file_names
    return path_dict


def read_files(cand_name, ref_names):
    references = []
    # print '\n\nREAD FILES'
    # print cand_name
    # print ref_names
    if os.path.isdir(ref_names):
        # print '\n\nIS DIR'
        # ref_files = [x for x in os.walk(ref_names)]
        # print ref_files
        for root, dirs, files in os.walk(ref_names):
            for f in files:
                # print f
                temp_file = codecs.open(os.path.join(root, f), 'r', 'utf-8')
                # print 'Reading %s' % os.path.join(root, f)
                references.append(temp_file.readlines())
    else:
        temp_file = codecs.open(ref_names, 'r', 'utf-8')
        references.append(temp_file.readlines())

    temp_file = codecs.open(cand_name, 'r', 'utf-8')
    candidate = temp_file.readlines()
    return candidate, references


def best_match_length(cand_len, ref_len):
    diff = float('inf')
    best_len = 0
    for ref in ref_len:
        if diff > abs(cand_len - ref):
            diff = abs(cand_len - ref)
            best_len = ref
    return best_len


def count_clip_ngram(candidate_dict, references_dicts):
    cnt = 0
    # Countclip = min(Count, Max_Ref_Count)
    for ngram in candidate_dict:
        cnd_ngram_cnt = candidate_dict[ngram]
        cnd_ngram_max = 0
        for ref_d in references_dicts:
            if ngram in ref_d:
                cnd_ngram_max = max(cnd_ngram_max, ref_d[ngram])
        cnd_ngram_cnt = min(cnd_ngram_cnt, cnd_ngram_max)
        cnt += cnd_ngram_cnt
    return cnt


def count_ngram(candidate, references, n):
    count_clipped = 0
    c = 0
    r = 0
    cand_ngram_cnt = 0
    for sentence_i in range(len(candidate)):
        ref_ngram_dicts = []
        ref_sen_lens = []

        curr_cand_sen = candidate[sentence_i]
        cand_word_list = curr_cand_sen.strip().split()
        cand_ngram_cnt += len(cand_word_list) - n + 1

        cand_ngram_dict = {}
        for i in range(len(cand_word_list) - n + 1):
            ngram = ''.join(cand_word_list[i:i + n]).lower()
            if ngram in cand_ngram_dict:
                cand_ngram_dict[ngram] += 1
            else:
                cand_ngram_dict[ngram] = 1

        for reference in references:

            curr_ref_sen = reference[sentence_i]
            print'************\n\n'
            print curr_ref_sen
            word_list = curr_ref_sen.strip().split()
            ref_sen_lens.append(len(word_list))

            ref_ngram_dict = {}
            for i in range(len(word_list) - n + 1):
                ngram = ''.join(word_list[i:i + n]).lower()
                if ngram in ref_ngram_dict:
                    ref_ngram_dict[ngram] += 1
                else:
                    ref_ngram_dict[ngram] = 1
            ref_ngram_dicts.append(ref_ngram_dict)
        count_clipped += count_clip_ngram(cand_ngram_dict, ref_ngram_dicts)
        r += best_match_length(len(cand_word_list), ref_sen_lens)
        c += len(cand_word_list)
    if count_clipped == 0:
        prec_n = 0
    else:
        prec_n = (1.0 * count_clipped) / cand_ngram_cnt

    # brev_penalty = brevity_penalty(c,r)
    if c > r:
        brev_penalty = 1
    else:
        brev_penalty = math.exp(1.0 - (r * 1.0 / c))

    return prec_n, brev_penalty


def calc_BLEU(candidate, references):
    ngram_prec = []
    # count uni-gram, bi-gram, tri-gram and tetra-gram precision
    prec_geo_mean = 1.0
    for i in range(1, 5, 1):
        prec_i, brev_penalty = count_ngram(candidate, references, i)
        prec_geo_mean *= prec_i

    prec_geo_mean = math.pow(prec_geo_mean, (1.0 / 4))
    bleu = prec_geo_mean * brev_penalty
    return bleu


def main():
    cand_name = sys.argv[1]
    ref_name = sys.argv[2]

    candidate, references = read_files(cand_name, ref_name)
    # print candidate
    # print len(candidate)
    # print references
    # print len(references)
    bleu_score = calc_BLEU(candidate, references)

    print bleu_score
if __name__ == '__main__':
    main()
