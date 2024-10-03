from tqdm import tqdm
import random
import json
import copy



def replace(item, semantic_id, manual_transcript, value, slots, data):
    for val in slots:
        item_new=copy.deepcopy(item)
        item_new["utt_id"] = 1
        item_new["semantic"][semantic_id][2] = val
        item_new['manual_transcript'] = manual_transcript.replace(value, val)
        data.append([item_new])
    return data

def replace_poi(item, semantic_id, manual_transcript, value, poi_names, data):
    val = random.choice(poi_names)
    item_new=copy.deepcopy(item)
    item_new["utt_id"] = 1
    item_new["semantic"][semantic_id][2] = val
    item_new['manual_transcript'] = manual_transcript.replace(value, val)
    data.append([item_new])
    return data
    

with open('./train_replaced.json', 'r') as f:
    train = json.load(f)

with open('./ontology.json', 'r') as f:
    ontology = json.load(f)
    
data = []

poi_slots = ['poi名称', 'poi修饰', 'poi目标', '起点名称', '起点修饰', '起点目标', '终点名称', '终点修饰', '终点目标', '途经点名称']

poi_names = [c.rstrip() for c in open('./lexicon/poi_name.txt')]

requests = ["附近", "定位", "近郊", "旁边", "周边", "就近", "最近"]

prefereneces = ["最近", "高速优先", "走国道", "少走高速", "不走高速", "走高速", "上高速", "高速公路", "最快", "躲避拥堵"]

num_poi = 30

for i in tqdm(range(len(train))):
    data.append(train[i])
    for item_id in range(len(train[i])):
        
        item = train[i][item_id]

        manual_transcript, semantic = item['manual_transcript'], item['semantic']

        for semantic_id in range(len(semantic)):
            slot, value = semantic[semantic_id][1], semantic[semantic_id][2]

            if value in manual_transcript: 
                if slot in poi_slots:
                    for j in range(num_poi):
                        data = replace_poi(item, semantic_id, manual_transcript, value, poi_names, data)
                        
                if slot == "路线偏好":
                    data = replace(item, semantic_id, manual_transcript, value, prefereneces, data)
            
                if slot == "请求类型":
                    data = replace(item, semantic_id, manual_transcript, value, requests, data)


train_augment = json.dumps(data, indent=4, ensure_ascii=False)

with open('./train_augment_asr.json', 'w') as wf:
    print(train_augment, file=wf)
                
                