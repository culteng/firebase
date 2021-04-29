''' this module interacts with firestore  - https://firebase.google.com/docs/firestore/manage-data/add-data
example manaul load, auto generate id:
question = SurveyQuestion(text=u'How do you feel?', qtype=u'likert')
db.collection(u'survey_questions').add(city.to_dict())

to set creds on powershell :  # https://cloud.google.com/docs/authentication/getting-started#windows
$env:GOOGLE_APPLICATION_CREDENTIALS="./cultural engagement-f2d38a123f26.json"
then sample run:
python .\add_question.py -t .\questions.txt
'''

import argparse
import sys
from csv import reader
from google.cloud import firestore # pip google-cloud-firestore


def parse_args(args):
    parser = argparse.ArgumentParser(
        description='arguments to provide to main()',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument('-m', '--mode', default='csv')
    parser.add_argument('-t', '--target')

    return parser.parse_args(args)

class SurveyQuestion(object):
    def __init__(self, text, qtype, construct):
        self.text = text
        self.qtype = qtype
        self.construct = construct
        
    @staticmethod
    def from_dict(source):
        question = SurveyQuestion(
                    source[u'text'], 
                    source[u'qtype'], 
                    source[u'construct'])

        return question

    def to_dict(self):
        dest = {
            u'text': self.text,
            u'qtype': self.qtype,
            u'construct': self.construct
        }

        return dest

    def __repr__(self):
        return(
            f'City(\
                text={self.text}, \
                qtype={self.qtype}, \
                construct={self.construct}, \
            )'
        )
        

def main(args):
    pargs = parse_args(args)
    db = firestore.Client()
    if pargs.mode == 'csv':
        with open(pargs.target, 'r') as read_obj:
            csv_reader = reader(read_obj, delimiter='\t')
            headers = next(csv_reader)
            for row in csv_reader:
                question = SurveyQuestion(
                text=row[0],
                qtype=row[1],
                construct=row[2])
                db.collection(u'survey_questions').add(question.to_dict())


if __name__ == '__main__':
    main(sys.argv[1:])