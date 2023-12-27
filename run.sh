# slu_tagging
python -X utf8 main.py --model slu_tagging --device 0 --encoder_cell RNN
python -X utf8 main.py --model slu_tagging --device 0 --encoder_cell LSTM
python -X utf8 main.py --model slu_tagging --device 0 --encoder_cell GRU
python -X utf8 main.py --model slu_tagging --device 0 --testing --testing_path ./ckpt/slu_tagging/train_xxxxxxxxxxxxxx/slu_tagging.bin

# slu_bert
python -X utf8 main.py --model slu_bert --device 0 --lr 5e-5 --optimizer AdamW --scheduler
python -X utf8 main.py --model slu_bert --device 0 --testing --testing_path ./ckpt/slu_bert/train_xxxxxxxxxxxxxx/slu_bert.bin

# slu_bert_rnn
python -X utf8 main.py --model slu_bert_rnn --device 0 --lr 5e-5 --optimizer AdamW --scheduler --encoder_cell RNN
python -X utf8 main.py --model slu_bert_rnn --device 0 --lr 5e-5 --optimizer AdamW --scheduler --encoder_cell LSTM
python -X utf8 main.py --model slu_bert_rnn --device 0 --lr 5e-5 --optimizer AdamW --scheduler --encoder_cell GRU
