# -*- coding: utf-8 -*-
#2018/11/16 富文本格式转换
#2018/11/17,19 添加ini配置文件支持

__author__='gamefang'
version='v1.0.4'

import codecs

#加载配置并全局化
import configparser
cfg=configparser.ConfigParser()
cfg.read('parser.ini',encoding='utf8')
cfg={ **cfg._defaults,**cfg._sections }

def parser(richtext,rules):
    '''
    单行文本转换。
    @param richtext: 特殊标记的单行字符串
    @param rules: 转换规则字典
    @return: 格式化后的字符串
    '''
    texts=richtext.split(rules['separator'])
    signs=[item for item in rules.keys() if len(item)==1]
    new_texts=[]
    for text in texts:
        text=text.strip()
        if not text:    #跳过空行
            new_texts.append('')
            continue
        if text.startswith(tuple(signs)):  #特殊渲染
            new_text = rules[text[0]] + text[1:] + rules['normal_suf']
        else:   #普通渲染
            new_text = rules['normal_pre'] + text + rules['normal_suf']
        #处理换行符
        new_text=new_text.replace('\\n','\n')
        new_text=new_text.replace('\r\n','')
        new_text=repr(new_text)[1:-1]
        new_texts.append(new_text)
    return ','.join(new_texts)

def main(cfg):
    with codecs.open(cfg['input_file'],'r','utf8') as f:
        rich_texts=[parser(text,cfg['rules']) for text in f.readlines()]
    with codecs.open(cfg['output_file'],'w','utf8') as f:
        for text in rich_texts:
            f.write(text+'\n')
    print('<%s> done!' % cfg['output_file'])
    
if __name__ == '__main__':
    main(cfg)
