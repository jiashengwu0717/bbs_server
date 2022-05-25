# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

class BbsProjectPipeline(object):
    def process_item(self, item, spider):
        return item

class BbsProjectInfoPipeline(object):
    def open_spider(self,spider):
        self.f = open('bbs_server.txt', 'w')

    def close_spider(self,spider):
        self.f.close()

    def process_item(self,item,spider):
        try:
            for key in dict(item):
                if key == '71':
                    if '出' in dict(item)[71][3]:
                        self.f.write(' '.join(dict(item)[71]))
                        self.f.write('\r\n')
                elif key == '242':
                    if '招募' in dict(item)[242][3]:
                        self.f.write(' '.join(dict(item)[242]))
                        self.f.write('\r\n')
                elif key == '914':
                    if '出' in dict(item)[914][3] or '转' in dict(item)[914][3] or '送' in dict(item)[914][3]:
                        self.f.write(' '.join(dict(item)[914]))
                        self.f.write('\r\n')
                else:
                    self.f.write(' '.join(dict(item)[key]))
                    self.f.write('\r\n')               # 将返回的内容写入bbs_server.txt文件
        except:
            pass
        return item



