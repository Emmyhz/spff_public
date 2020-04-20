import jieba
from data.server import Data
import json
from common.common import common_tools as common




strip_word_list = ['\n',' ']


def split_case_info(case):
    title = case['title']
    content = json.loads(case['content'])
    title_list = list(jieba.cut_for_search(title))
    content_list = list(jieba.cut_for_search(content))

    case_list = title_list+content_list
    case_word_list = list(set(case_list))

    # print(case_list)
    for word in case_word_list:
        if word not in strip_word_list:
            word_md5 = common.get_md5(word)
            res = Data.find('case_search_index',[('case_id','=',case['id']),('keyword_md5','=',word_md5)])
            if res != None:
                print('已经存在')
                continue
            params = {
                'case_id':case['id'],
                'keyword':json.dumps(word),
                'keyword_md5':word_md5
            }
            Data.insert('case_search_index',params)
            continue
        else:
            continue



    # for i in case_list:

# def 
all_case = Data.select('case_info',[('id','!=',0)])

for case in all_case:
    split_case_info(case)

from data.server import Data
from common.common import common_tools as common

def kill_md():
    all_info = Data.select('case_info',[('id','!=',0)])
    for line in all_info:
        res = common.decode_base64(line['title'])
        # print(res)
        case_title_list = res.split('.')
        if len(case_title_list) >=2:
            if case_title_list[1] == 'md':
                print(case_title_list[0])
                new_title = common.get_base64(case_title_list[0].encode('utf-8'))
                Data.update('case_info',[('id','=',line['id'])],{'title':new_title})

