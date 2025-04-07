#Obtain raw data
python ./mem-chinese-kk-logic/data_gen_kk.py

#Process raw data
for ppl in 3 4 5 6 7 8
do
    python ./examples/data_preprocess/kk_cn.py --local_dir ./data/kk-cn/instruct/${ppl}ppl/ --data_path /mnt/userdata/tanyuqiao/Chinese_Logic_R1/data/kk-cn-raw/train/clean/people${ppl}_num1000.jsonl --template_type qwen-instruct
done

#Merge all ppl
cd ./data/kk-cn/instruct/
python merge.py