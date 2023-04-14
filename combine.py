#before run this code, you need to pip install requests

import requests, uuid, json

# 連番のJSONLファイル名を生成する
start = 0
end = 15000
step = 100
jsonl_files = [f"databricks-dolly-15k_ja_{i}_{i+step}.jsonl" for i in range(start, end, step)]
jsonl_files.append(f"databricks-dolly-15k_ja_15000_15015.jsonl")

# 各JSONLファイルを読み込み、各行を辞書オブジェクトに変換してリストに追加する
merged_data = []
for jsonl_file in jsonl_files:
    with open(jsonl_file, "r", encoding="utf-8") as f:
        for line in f:
            data = json.loads(line)
            merged_data.append(data)

# リストに追加された辞書オブジェクトを新しいJSONLファイルに書き込む
with open("databricks-dolly-15k_ja.jsonl", "w", encoding="utf-8") as f:
    for data in merged_data:
        json_line = json.dumps(data, ensure_ascii=False)
        f.write(json_line + "\n")

# ログファイル名
log_file = "example.log"

# "skip"を含む行を抽出する
with open(log_file, "r") as f:
    lines = f.readlines()
    skip_lines = [line for line in lines if "skip" in line]

# "skip"を含む行から数値を抽出し、整数型に変換してリストに追加する
skip_numbers = []
for line in skip_lines:
    if "skip" in str(line):
        number = int(line.split("skip")[1].split()[0])
        skip_numbers.append(number)

# 英語版のjsonファイルを読み込む
with open("databricks-dolly-15k.jsonl", 'r') as f:
    data = [json.loads(l) for l in f.readlines()]

# fuguMTで翻訳出来なかった行をMicrosoft Azureの翻訳を利用するための設定
key = "<azure_translator_api_key>"
endpoint = "https://api.cognitive.microsofttranslator.com"

# location, also known as region.
# required if you're using a multi-service or regional (not global) resource. It can be found in the Azure portal on the Keys and Endpoint page.
location = "<your_location>"

path = '/translate'
constructed_url = endpoint + path

params = {
    'api-version': '3.0',
    'from': 'en',
    'to': ['ja']
}

headers = {
    'Ocp-Apim-Subscription-Key': key,
    # location required if you're using a multi-service or regional (not global) resource.
    'Ocp-Apim-Subscription-Region': location,
    'Content-type': 'application/json',
    'X-ClientTraceId': str(uuid.uuid4())
}

for s in skip_numbers:
# You can pass more than one object in body.
    body = [{
        'text': data[s]['instruction']
        }]

    request = requests.post(constructed_url, params=params, headers=headers, json=body)
    response = request.json()
    instruction = repr(response[0]["translations"][0]["text"])

    body = [{
        'text': data[s]['context']
        }]

    request = requests.post(constructed_url, params=params, headers=headers, json=body)
    response = request.json()
    context = repr(response[0]["translations"][0]["text"])

    body = [{
        'text': data[s]['response']
        }]

    request = requests.post(constructed_url, params=params, headers=headers, json=body)
    response = request.json()
    res = repr(response[0]["translations"][0]["text"])


    body = [{
        'text': data[s]['category']
        }]

    request = requests.post(constructed_url, params=params, headers=headers, json=body)
    response = request.json()
    category = repr(response[0]["translations"][0]["text"])

    line = '{"instruction": "' + instruction + '", "context": "' + context + '", "response": "' + res + '", "category": "' + category + '"}'

    print(line)

#あとはprintしたものを手動コピペで目視確認しながらjsonlファイルに書き込む！ 最後は目視！