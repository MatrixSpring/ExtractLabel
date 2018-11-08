from pandas.io.json import json

from app.src.extraction.triple_extraction_utils import TripleExtractor
from app.src.markrecord.markrecord import MarkRecord
from app.src.utils.fileutils import loadLine

if __name__ == '__main__':
    source_path = '../../res/foo.txt'
    save_path = '../../assert/foo-all.txt'

    extractor = TripleExtractor()
    markrecord = MarkRecord()

    content6 = '本月赎回倚天阁，给她寄送资料，今天寄'
    svos = extractor.triples_main(content6)
    print('svos', svos)

    total_score = markrecord.mark_record(svos)
    print('total_score', total_score)

    list_remark = loadLine('../../res/foo.txt')

    fp = open('../../assert/tree-triple-extractor-5.txt', "w", encoding='utf-8', errors='ignore')
    for item_data in list_remark:
        in_json = json.loads(item_data)  # Encode the data
        remarks = in_json['remarks'] if in_json['remarks'] else " "
        if remarks != '':
            custom_state = in_json['custom_state'] if in_json['custom_state'] else " "
            # out_json = {}
            # out_json["custom_state"] = custom_state
            # out_json["remarks"] = remarks

            svos = extractor.triples_main(remarks)
            total_score = markrecord.mark_record(svos)
            # print('svos', remarks, str(svos))
            # if len(svos):
            #     content = ", ".join(svos)
            # else:
            #     content = svos
            fp.write(custom_state + '\t' +str(total_score) + '\t' + remarks + '\t' + str(svos) + '\n')
    fp.close()
