''' this module interacts with firestore  - https://firebase.google.com/docs/firestore/manage-data/add-data
good reference: https://rominirani.com/build-a-serverless-online-quiz-with-google-cloud-functions-and-cloud-firestore-1e3fbf84a7d8
example ____:
question = Survey
db.coll

to set creds on powershell :  # https://cloud.google.com/docs/authentication/getting-started#windows
sample run:
python .\add_survey.py -m constructs -c purpose belonging fairness faith opportunities leadership
'''

import argparse
import sys
from google.cloud import firestore

db = firestore.Client()

def parse_args(args):
    parser = argparse.ArgumentParser(
        description='arguments to provide to main()',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument('-m', '--mode', default='constructs')
    parser.add_argument('-c', '--constructs', default=['purpose', 'belonging', 'fairness', 'faith', 'opportunities', 'leadership'], nargs="+" )

    return parser.parse_args(args)


def retrieve_by_construct(construct):
    qs = []
    query = db.collection(u'survey_questions').where(u'construct', u'==', u'{}'.format(construct))
    for q in query.stream():
        qs.append((q.id, q.to_dict()))
        
    return qs



def main(args):
    pargs = parse_args(args)
    new_survey_ref = db.collection(u'surveys').document()
    if pargs.mode == 'constructs':
        for cn, construct in enumerate(pargs.constructs):
            qs_dict = {}
            new_construct_ref = new_survey_ref.collection(u'constructs').document(u'{}'.format(construct))
            qs = retrieve_by_construct(construct)
            for qn, q in enumerate(qs):
                qid, qdict = q
                qs_dict.update({
                u'q.{}.{}'.format(cn,qn):  {
                u'id':qid,
                u'text': qdict[u'text'],
                u'qtype': qdict[u'qtype']
                }})
            new_construct_ref.set(qs_dict)
                


if __name__ == '__main__':
    main(sys.argv[1:])