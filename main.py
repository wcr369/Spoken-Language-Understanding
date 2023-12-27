import os
import sys
import time
import json
import numpy as np
import torch
from torch.optim import Adam, AdamW
from torch.optim.lr_scheduler import StepLR

from utils.vocab import PAD
from utils.args import init_args
from utils.batch import from_example_list
from utils.init import set_random_seed, set_torch_device
from utils.example import Example
from utils.logger import Logger
from model.slu_tagging import SLUTagging
from model.slu_bert import SLUBert


# init args
args = init_args(sys.argv[1:])
if not args.testing:
    ckpt_path = f'./ckpt/{args.model}/train_{time.strftime("%Y%m%d%H%M%S", time.localtime())}'
else:
    ckpt_path = f'./ckpt/{args.model}/test_{time.strftime("%Y%m%d%H%M%S", time.localtime())}'
os.makedirs(ckpt_path, exist_ok=True)
sys.stdout = Logger(os.path.join(ckpt_path, f'{args.model}.log'))
print('-' * 50)
for k, v in vars(args).items():
    print(f'{k}: {v}')
print('-' * 50, '\n')
set_random_seed(args.seed)
device = set_torch_device(args.device)
args.device_name = device
print('-' * 50)
print('Initialization finished ...')
print(f'Random seed is set to {args.seed}')
if args.device >= 0:
    print(f'Use GPU with index {args.device}')
else:
    print('Use CPU as target torch device')

# load dataset
start_time = time.time()
train_path = os.path.join(args.dataroot, 'train.json')
dev_path = os.path.join(args.dataroot, 'development.json')
Example.configuration(args.dataroot, train_path=train_path, word2vec_path=args.word2vec_path)
train_dataset = Example.load_dataset(train_path)
dev_dataset = Example.load_dataset(dev_path)
args.vocab_size = Example.word_vocab.vocab_size
args.num_tags = Example.label_vocab.num_tags
args.pad_idx = Example.word_vocab[PAD]
args.tag_pad_idx = Example.label_vocab.convert_tag_to_idx(PAD)
print(f'Load dataset and database finished, cost {time.time() - start_time:.4f}s')
print(f'Dataset size: train -> {len(train_dataset)}, dev -> {len(dev_dataset)}')

# init model
if args.model == 'slu_tagging':
    model = SLUTagging(args).to(device)
    Example.word2vec.load_embeddings(model.word_embed, Example.word_vocab, device=device)
elif args.model == 'slu_bert':
    args.bert_path = './model/bert_base_chinese'
    model = SLUBert(args).to(device)
else:
    raise NotImplementedError(f'no model named {args.model}')
if args.testing:
    ckpt = torch.load(args.testing_path, map_location=device)
    model.load_state_dict(ckpt['model'])
    print(f'Load saved model from {args.testing_path} finished')

# init optimizer
if args.optimizer == 'Adam':
    optimizer = Adam(model.parameters(), lr=args.lr)
elif args.optimizer == 'AdamW':
    optimizer = AdamW(model.parameters(), lr=args.lr)
else:
    raise NotImplementedError(f'no optimizer named {args.optimizer}')
if args.scheduler:
    scheduler = StepLR(optimizer, step_size=10, gamma=0.8)
print('-' * 50, '\n')


def decode(choice):
    assert choice in ['train', 'dev']
    model.eval()
    dataset = train_dataset if choice == 'train' else dev_dataset
    predictions, labels = [], []
    total_loss, count = 0, 0
    with torch.no_grad():
        for i in range(0, len(dataset), args.batch_size):
            cur_dataset = dataset[i: i + args.batch_size]
            current_batch = from_example_list(args, cur_dataset, device, train=True)
            pred, label, loss = model.decode(Example.label_vocab, current_batch)
            for j in range(len(current_batch)):
                if any([l.split('-')[-1] not in current_batch.utt[j] for l in pred[j]]):
                    print(current_batch.utt[j], pred[j], label[j])
            predictions.extend(pred)
            labels.extend(label)
            total_loss += loss
            count += 1
        metrics = Example.evaluator.acc(predictions, labels)
    return metrics, total_loss / count


def predict():
    model.eval()
    test_path = os.path.join(args.dataroot, 'test_unlabelled.json')
    test_dataset = Example.load_dataset(test_path)
    predictions = {}
    with torch.no_grad():
        for i in range(0, len(test_dataset), args.batch_size):
            cur_dataset = test_dataset[i: i + args.batch_size]
            current_batch = from_example_list(args, cur_dataset, device, train=False)
            pred = model.decode(Example.label_vocab, current_batch)
            for pi, p in enumerate(pred):
                did = current_batch.did[pi]
                predictions[did] = p
    test_json = json.load(open(test_path, 'r'))
    ptr = 0
    for ei, example in enumerate(test_json):
        for ui, utt in enumerate(example):
            utt['pred'] = [pred.split('-') for pred in predictions[f'{ei}-{ui}']]
            ptr += 1
    json.dump(test_json, open(os.path.join(ckpt_path, f'{args.model}.json'), 'w',encoding='utf-8'), indent=4, ensure_ascii=False)


def train():
    print('-' * 50)
    num_training_steps = ((len(train_dataset) + args.batch_size - 1) // args.batch_size) * args.max_epoch
    print('Total training steps: %d' % (num_training_steps))
    nsamples, best_result = len(train_dataset), {'dev_acc': 0., 'dev_f1': 0.}
    train_index, step_size = np.arange(nsamples), args.batch_size
    print('Start training ......\n')

    for i in range(args.max_epoch):
        start_time = time.time()
        np.random.shuffle(train_index)
        epoch_loss, count = 0, 0
        model.train()
        for j in range(0, nsamples, step_size):
            cur_dataset = [train_dataset[k] for k in train_index[j: j + step_size]]
            current_batch = from_example_list(args, cur_dataset, device, train=True)
            output, loss = model(current_batch)
            loss.backward()
            optimizer.step()
            optimizer.zero_grad()
            epoch_loss += loss.item()
            count += 1
        print(f'Training: \tEpoch: {i}\tTime: {time.time() - start_time:.4f}\tTraining Loss: {epoch_loss / count:.4f}')

        start_time = time.time()
        metrics, dev_loss = decode('dev')
        dev_acc, dev_fscore = metrics['acc'], metrics['fscore']
        print(f'Evaluation: \tEpoch: {i}\tTime: {time.time() - start_time:.4f}\tDev acc: {dev_acc:.2f}\tDev fscore(p/r/f): ({dev_fscore["precision"]:.2f}/{dev_fscore["recall"]:.2f}/{dev_fscore["fscore"]:.2f})')
        if dev_acc > best_result['dev_acc']:
            best_result['dev_loss'], best_result['dev_acc'], best_result['dev_f1'], best_result['iter'] = dev_loss, dev_acc, dev_fscore, i
            torch.save({'epoch': i, 'model': model.state_dict(), 'optim': optimizer.state_dict()}, os.path.join(ckpt_path, f'{args.model}.bin'))
            print(f'NEW BEST MODEL: \tEpoch: {i}\tDev loss: {dev_loss:.4f}\tDev acc: {dev_acc:.2f}\tDev fscore(p/r/f): ({dev_fscore["precision"]:.2f}/{dev_fscore["recall"]:.2f}/{dev_fscore["fscore"]:.2f})')
        
        if args.scheduler:
            scheduler.step()
        print()

    print(f'FINAL BEST RESULT: \tEpoch: {best_result["iter"]}\tDev loss: {best_result["dev_loss"]:.4f}\tDev acc: {best_result["dev_acc"]:.2f}\tDev fscore(p/r/f): ({best_result["dev_f1"]["precision"]:.2f}/{best_result["dev_f1"]["recall"]:.2f}/{best_result["dev_f1"]["fscore"]:.2f})')
    print('-' * 50, '\n')


def test():
    print('-' * 50)
    start_time = time.time()
    metrics, dev_loss = decode('dev')
    dev_acc, dev_fscore = metrics['acc'], metrics['fscore']
    predict()
    print(f'Evaluation costs {time.time() - start_time:.2f}s ; Dev loss: {dev_loss:.4f}\tDev acc: {dev_acc:.2f}\tDev fscore(p/r/f): ({dev_fscore["precision"]:.2f}/{dev_fscore["recall"]:.2f}/{dev_fscore["fscore"]:.2f})')
    print('-' * 50, '\n')


if not args.testing:
    train()
else:
    test()
