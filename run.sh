# slu_tagging
python -X utf8 main.py --model slu_tagging --device 0
python -X utf8 main.py --model slu_tagging --device 0 --testing --testing_path ./ckpt/slu_tagging/train_xxxxxxxxxxxxxx/slu_tagging.bin

# slu_bert
python -X utf8 main.py --model slu_bert --device 0 --lr 5e-5 --optimizer AdamW --scheduler
python -X utf8 main.py --model slu_bert --device 0 --testing --testing_path ./ckpt/slu_bert/train_xxxxxxxxxxxxxx/slu_bert.bin
