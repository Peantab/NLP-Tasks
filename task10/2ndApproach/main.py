from fastai.text import MultiBatchRNN, SequentialRNN, LinearDecoder, Dataset, load_model, SortSampler, DataLoader,\
    no_grad_context
import numpy as np
import torch
import sentencepiece as spm

# Solution adapted from: https://github.com/JakDar/nlp-lab-2019/blob/master/lab10/Lab10.ipynb

root = '../v50knl4/work/up_low50k/'
fastai_model_path = root + 'models/fwd_v50k_finetune_lm_enc.h5'
sentencepiece_model_path = root + 'tmp/sp-50k.model'
sentencepiece_vocab_path = root = 'tmp/sp-50k.vocab'
PAD_ID = 1  # the int value used for padding text


def main():
    spm_processor = init_sentencepiece()
    lm = init_language_model(spm_processor)

    declension = [
        "Warszawa to największe ",
        "Te zabawki należą do ",
        "Policjant przygląda się ",
        "Na środku skrzyżowania widać ",
        "Właściciel samochodu widział złodzieja z ",
        "Prezydent z premierem rozmawiali wczoraj o ",
        "Witaj drogi "
    ]

    gender = [
        "Gdybym wiedział wtedy dokładnie to co wiem teraz, to bym się nie ",
        "Gdybym wiedziała wtedy dokładnie to co wiem teraz, to bym się nie "
    ]

    creation = "Polscy naukowcy odkryli w Tatrach nowy gatunek istoty żywej. " \
               "Zwięrzę to przypomina małpę, lecz porusza się na dwóch nogach i potrafi posługiwać się narzędziami. " \
               "Przy dłuższej obserwacji okazało się, że potrafi również posługiwać się językiem polskim, " \
               "a konkretnie gwarą podhalańską. Zwierzę to zostało nazwane "

    print_results("DEKLINACJA:", declension, lm, spm_processor)
    print_results("RODZAJE:", gender, lm, spm_processor)
    print_results("Dokończenie zdania:", [creation], lm, spm_processor)


def init_sentencepiece():
    spm_processor = spm.SentencePieceProcessor()
    spm_processor.Load(sentencepiece_model_path)

    spm_processor.SetEncodeExtraOptions("bos:eos")  # add <s> and </s>.
    spm_processor.SetDecodeExtraOptions("bos:eos")

    return spm_processor


def init_language_model(spm_processor):
    bptt = 5  # Backpropagation through time
    max_seq = 50
    vs = len(spm_processor)
    emb_sz = 400  # the embedding size to use to encode each token
    n_hid = 1150  # number of hidden activation per LSTM layer
    n_layers = 4  # number of LSTM layers to use in the architecture

    lm = get_lm(bptt, max_seq, vs, emb_sz, n_hid, n_layers, PAD_ID)
    load_model(lm[0], fastai_model_path)
    lm.reset()
    lm.eval()
    return lm


def get_lm(bptt, max_seq, n_tok, emb_sz, n_hid, n_layers, pad_token, bidir=False,
           tie_weights=True, qrnn=False):
    rnn_enc = MultiBatchRNN(bptt, max_seq, n_tok, emb_sz, n_hid, n_layers, pad_token=pad_token, bidir=bidir, qrnn=qrnn)
    enc = rnn_enc.encoder if tie_weights else None
    return SequentialRNN(rnn_enc, LinearDecoder(n_tok, emb_sz, 0, tie_encoder=enc))


class LMTextDataset(Dataset):
    def __init__(self, x):
        self.x = x

    def __getitem__(self, idx):
        sentence = self.x[idx]
        return sentence[:-1], sentence[1:]

    def __len__(self):
        return len(self.x)


def next_tokens(ids_, model, deterministic, omit_ids=[]):
    ids = [np.array(ids_)]
    test_ds = LMTextDataset(ids)
    test_samp = SortSampler(ids, key=lambda x: len(ids[x]))
    bs = 22
    dl = DataLoader(test_ds,
                    bs,
                    transpose=True,
                    transpose_y=True,
                    num_workers=1,
                    pad_idx=PAD_ID,
                    sampler=test_samp,
                    pre_pad=False)

    tensor1 = None
    with no_grad_context():
        for (x, y) in dl:
            tensor1 = model(x)
    p = tensor1[0]

    arg = p[-1]
    r = int(
        torch.argmax(arg) if deterministic else torch.
        multinomial(p[-1].exp(), 1))  # probability is in logharitm

    while r in omit_ids + [ids_[-1]]:
        arg[r] = -1
        r = int(torch.argmax(arg))

    predicted_ids = [r]
    return predicted_ids


def next_words_best(ss, lm, spm_processor, n_words=70, is_deterministic=True, omit_ids=[]):
    ss_ids = spm_processor.encode_as_ids(ss)
    wip = ss
    wip_ids = ss_ids
    for i in range(n_words):
        next_ = next_tokens(wip_ids, lm, is_deterministic, omit_ids=omit_ids)
        wip_ids = wip_ids + next_
        wip = spm_processor.decode_ids(wip_ids)
        wip_ids = spm_processor.encode_as_ids(wip)

    return wip


def print_results(category, sentences, lm, spm_processor):
    print(category)
    for sentence in sentences:
        print(next_words_best(sentence, lm, spm_processor, is_deterministic=False))
    print()


if __name__ == '__main__':
    main()
