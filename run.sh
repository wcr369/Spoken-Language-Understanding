# slu_tagging
python -X utf8 main.py --model slu_tagging --device 0 --encoder_cell RNN
python -X utf8 main.py --model slu_tagging --device 0 --encoder_cell RNN --testing
python -X utf8 main.py --model slu_tagging --device 0 --encoder_cell LSTM
python -X utf8 main.py --model slu_tagging --device 0 --encoder_cell LSTM --testing
python -X utf8 main.py --model slu_tagging --device 0 --encoder_cell GRU
python -X utf8 main.py --model slu_tagging --device 0 --encoder_cell GRU --testing

# slu_transformer
python -X utf8 main.py --model slu_transformer --device 0  --num_layer 6  --lr 5e-5 --optimizer AdamW
python -X utf8 main.py --model slu_transformer --device 0 --num_layer 6 --testing

# slu_rnn_crf
python -X utf8 main.py --model slu_rnn_crf --device 0 --encoder_cell RNN
python -X utf8 main.py --model slu_rnn_crf --device 0 --encoder_cell RNN --testing
python -X utf8 main.py --model slu_rnn_crf --device 0 --encoder_cell LSTM
python -X utf8 main.py --model slu_rnn_crf --device 0 --encoder_cell LSTM --testing
python -X utf8 main.py --model slu_rnn_crf --device 0 --encoder_cell GRU
python -X utf8 main.py --model slu_rnn_crf --device 0 --encoder_cell GRU --testing

# slu_bert
python -X utf8 main.py --model slu_bert --device 0 --lr 2e-3 --optimizer AdamW
python -X utf8 main.py --model slu_bert --device 0 --testing

# slu_bert_rnn
python -X utf8 main.py --model slu_bert_rnn --device 0 --encoder_cell RNN --lr 2e-3 --optimizer AdamW
python -X utf8 main.py --model slu_bert_rnn --device 0 --encoder_cell RNN --testing
python -X utf8 main.py --model slu_bert_rnn --device 0 --encoder_cell LSTM --lr 2e-3 --optimizer AdamW
python -X utf8 main.py --model slu_bert_rnn --device 0 --encoder_cell LSTM --testing
python -X utf8 main.py --model slu_bert_rnn --device 0 --encoder_cell GRU --lr 2e-3 --optimizer AdamW
python -X utf8 main.py --model slu_bert_rnn --device 0 --encoder_cell GRU --testing

# slu_bert_crf
python -X utf8 main.py --model slu_bert_crf --device 0 --lr 2e-3 --optimizer AdamW
python -X utf8 main.py --model slu_bert_crf --device 0 --testing

# slu_bert_rnn_crf
python -X utf8 main.py --model slu_bert_rnn_crf --device 0 --encoder_cell RNN --lr 2e-3 --optimizer AdamW
python -X utf8 main.py --model slu_bert_rnn_crf --device 0 --encoder_cell RNN --testing
python -X utf8 main.py --model slu_bert_rnn_crf --device 0 --encoder_cell LSTM --lr 2e-3 --optimizer AdamW
python -X utf8 main.py --model slu_bert_rnn_crf --device 0 --encoder_cell LSTM --testing
python -X utf8 main.py --model slu_bert_rnn_crf --device 0 --encoder_cell GRU --lr 2e-3 --optimizer AdamW
python -X utf8 main.py --model slu_bert_rnn_crf --device 0 --encoder_cell GRU --testing

# add --correction for correction
