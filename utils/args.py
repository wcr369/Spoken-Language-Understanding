import sys
import argparse


def add_argument_base(arg_parser):
    # general
    arg_parser.add_argument('--model', default='slu_tagging', choices=['slu_tagging', 'slu_bert', 'slu_bert_rnn','slu_transformer'], help='model name')
    arg_parser.add_argument('--dataroot', default='./data', help='root of data')
    arg_parser.add_argument('--seed', default=114514, type=int, help='Random seed')
    arg_parser.add_argument('--device', type=int, default=-1, help='Use which device: -1 -> cpu ; the index of gpu o.w.')
    arg_parser.add_argument('--testing', action='store_true', help='training or evaluation mode')
    arg_parser.add_argument('--testing_path', default=None, help='path of testing model')
    # training
    arg_parser.add_argument('--batch_size', default=32, type=int, help='Batch size')
    arg_parser.add_argument('--lr', type=float, default=1e-3, help='learning rate')
    arg_parser.add_argument('--max_epoch', type=int, default=100, help='terminate after maximum epochs')
    arg_parser.add_argument('--optimizer', default='Adam', choices=['Adam', 'AdamW'], help='optimizer')
    arg_parser.add_argument('--scheduler', action='store_true', help='whether to use scheduler')
    arg_parser.add_argument('--num_heads', default=8, type=int, help='number of head')
    # model
    arg_parser.add_argument('--encoder_cell', default='RNN', choices=['RNN', 'LSTM', 'GRU'], help='root of data')
    arg_parser.add_argument('--dropout', type=float, default=0.2, help='feature dropout rate')
    arg_parser.add_argument('--embed_size', default=768, type=int, help='Size of word embeddings')
    arg_parser.add_argument('--hidden_size', default=512, type=int, help='hidden size')
    arg_parser.add_argument('--num_layer', default=2, type=int, help='number of layer')
    return arg_parser


def init_args(params=sys.argv[1:]):
    arg_parser = argparse.ArgumentParser()
    arg_parser = add_argument_base(arg_parser)
    opt = arg_parser.parse_args(params)
    return opt
