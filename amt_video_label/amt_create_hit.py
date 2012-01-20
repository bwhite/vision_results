import boto
import boto.mturk.qualification
import os

kw = {}
#kw = {'host': 'mechanicalturk.sandbox.amazonaws.com'}
mtc = boto.connect_mturk(os.environ['AWS_ACCESS_KEY_ID'], os.environ['AWS_SECRET_ACCESS_KEY'], **kw)

question = boto.mturk.question.ExternalQuestion('http://api.dappervision.com:8000', 1200)
qualifications = boto.mturk.qualification.Qualifications()
qualifications.add(boto.mturk.qualification.PercentAssignmentsApprovedRequirement('GreaterThan', 80, True))
qualifications.add(boto.mturk.qualification.NumberHitsApprovedRequirement('GreaterThan', 100, True))
out = mtc.create_hit(question=question,
                     max_assignments=10,
                     qualifications=qualifications,
                     title='Video Topic Annotation',
                     description='Categorize videos by topic (shown as a selection of frames).',
                     keywords='video annotation'.split(),
                     duration = 60 * 30,
                     reward=0.10)
