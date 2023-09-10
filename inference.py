import pandas as pd
import regex as re
from tqdm import tqdm
tqdm.pandas()

from analyzer import TextAnalyzer


analyzer_obj = TextAnalyzer()
filename = ''
text_column = ''

if filename.split('.')[-1] == 'xlsx':
    data = pd.read_excel(filename)
else:
    data = pd.read_csv(filename)

possible_subjects_list = []
for index, row in tqdm(data.iterrows()):
    possible_subjects = ''
    for text in re.split(' *[.!?] *', row[text_column]):
        subject = analyzer_obj.extract_subject(text)
        if not subject:
            continue
        # try:
        possible_subjects+= ', '+subject
        # except Exception as e:
        #     print(possible_subjects, '\n', subject, '\n', e)
    possible_subjects_list.append(possible_subjects)

data['possible_subjects'] = possible_subjects_list
filename = filename.split('.')[0]
data.to_excel(filename+'_Output.xlsx', index=False)