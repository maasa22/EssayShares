# pipenv shell
# pipenv install firebase-admin
# https://qiita.com/yusukeito58/items/c77feaa25fbbe37e9953

import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import uuid
# import datetime
from datetime import datetime, timedelta, timezone
import random

# Use a service account
cred = credentials.Certificate('./essayshares-firebase-adminsdk-z8acj-afb9a3af99.json')
firebase_admin.initialize_app(cred)

db = firestore.client()

# create data
def createData():
    doc_ref = db.collection('essays').document(str(uuid.uuid4().hex))
    doc_ref.set({
        'essays': 'Most people agree that modern technology affects society in many different ways.  In my opinion, access to the Internet is enormously beneficial to both individuals and communities as a whole.  I feel this way for two reasons, which I will explore in the following essay.             To begin with, online investigative reporting helps to expose political corruption and keep politicians honest.  In the past, there were only a limited number of news outlets, which often had deep connections to powerful politicians. As a result, they were extremely hesitant to criticize them. These days, however, there are many independent publications on the Internet that are willing to expose political misbehavior.  For example, an online magazine recently published a story revealing that the mayor of my hometown had taken bribes from a property developer. The report was so detailed and well-researched that the mayor had no choice but to resign. Although the evidence was not difficult to locate, only this independent website was willing to write about it.  This example demonstrates how the Internet helps to strengthen democracy in the modern world.             Secondly, people are more motivated than ever to become politically active because they can freely exchange ideas online.  In countries all over the globe, people use social networking services to share their ideas and opinions. While in the past people might have thought that they were alone in their beliefs, today they realize that others share their ideas. My own experience demonstrates this concept.  When I was a university student, I learned that a municipal park near my apartment was going to be demolished to make room for a massive parking lot. This bothered me a lot because I enjoyed spending my free time in the park. At first I thought that there was nothing that I, as an individual, could do to stop this from happening.  However, I later joined a Facebook group dedicated to opposing the plan. When the members of the group learned how many people in the city loved the park we were happy to get together and enthusiastically protest in front of city hall until our voices were heard. I am convinced that finding each other on that social networking platform gave us the courage to actively protect our park.             In conclusion, I strongly believe that the Internet has a positive effect on our lives.  This sample is from https://www.toeflresources.com/sample-toefl-essays/. This is because online journalism strengthens our democracy, and because social networking sites encourage people to  get involved in local politics.',
        'createdAt' : datetime.datetime(1994, 2, 8, 1, 40, 27, 425337) ,\
        'topicNum' : 1, \
        'userId' : "userId", \
    })

# Read data
def readData():
    users_ref = db.collection('essays')
    docs = users_ref.stream()
    for doc in docs:
        print('{} => {}'.format(doc.id, doc.to_dict()))

# Update data

# Delete data
def deleteData():
    users_ref = db.collection(u'essays')
    docs = users_ref.limit(100).get()
    for doc in docs:
        print(u'Deleting doc {} => {}'.format(doc.id, doc.to_dict()))
        doc.reference.delete()


# readData()
deleteData()
# createData()

essayList = [ \
'Most people agree that modern technology affects society in many different ways.  In my opinion, access to the Internet is enormously beneficial to both individuals and communities as a whole.  I feel this way for two reasons, which I will explore in the following essay.             To begin with, online investigative reporting helps to expose political corruption and keep politicians honest.  In the past, there were only a limited number of news outlets, which often had deep connections to powerful politicians. As a result, they were extremely hesitant to criticize them. These days, however, there are many independent publications on the Internet that are willing to expose political misbehavior.  For example, an online magazine recently published a story revealing that the mayor of my hometown had taken bribes from a property developer. The report was so detailed and well-researched that the mayor had no choice but to resign. Although the evidence was not difficult to locate, only this independent website was willing to write about it.  This example demonstrates how the Internet helps to strengthen democracy in the modern world.             Secondly, people are more motivated than ever to become politically active because they can freely exchange ideas online.  In countries all over the globe, people use social networking services to share their ideas and opinions. While in the past people might have thought that they were alone in their beliefs, today they realize that others share their ideas. My own experience demonstrates this concept.  When I was a university student, I learned that a municipal park near my apartment was going to be demolished to make room for a massive parking lot. This bothered me a lot because I enjoyed spending my free time in the park. At first I thought that there was nothing that I, as an individual, could do to stop this from happening.  However, I later joined a Facebook group dedicated to opposing the plan. When the members of the group learned how many people in the city loved the park we were happy to get together and enthusiastically protest in front of city hall until our voices were heard. I am convinced that finding each other on that social networking platform gave us the courage to actively protect our park.             In conclusion, I strongly believe that the Internet has a positive effect on our lives.  This sample is from https://www.toeflresources.com/sample-toefl-essays/. This is because online journalism strengthens our democracy, and because social networking sites encourage people to  get involved in local politics.', \
 'It is critically important that students use the best available resources when they do research.  In my opinion, it is far better to use printed materials than online sources. I feel this way for two reasons, which I will explore in the following essay.           To begin with, printed materials such as books and articles are more reliable than websites.  This is because websites can be edited by anyone in the world, regardless of whether or not they are qualified academics.  As a result of this, even articles in popular online encyclopedias often contain incorrect and biased information. My own experience demonstrates the danger of relying too heavily on online sources of information.  Two semesters ago, I was assigned a research paper in a freshman biology class. I cited data that I found on Wikipedia which later turned out to be completely incorrect. This data was so hopelessly wrong that my professor spotted it immediately, causing me to fail the assignment and receive a fairly low grade in the class at the end of the semester.  If I had taken the time to compare what I had read online to a book or a scholarly article, I would not have included it, and would not have received such a terrible score in the class.          Secondly, books are superior to online articles because they cover topics in much detail.  Textbooks are significantly longer than online articles, so they are more useful to students.  Students who use them when doing projects can also look at the detailed indexes which they include to focus on very specific topics. For example, I was assigned an essay last semester in a history class and the very first book that I consulted contained a long description of both the underlying causes and long-term effects of the historical event I was writing about.  In contrast, most of the online articles that I consulted contained little more than superficial facts and dates. I based my research on the book rather than these articles, so I was able to write a very insightful paper.          In conclusion, I strongly believe that printed information is more useful than online resources.  This is because books and printed journals are less likely to be biased or contain errors, and because books provide a superior level of detail.', \
  'It is critically important that students work as hard as possible when they are at school.  Personally, I believe that teachers can motivate students to work hard by giving them grades. I feel this way for two reasons, which I will explore in the following essay.         To begin with, students who are graded achieve more comprehensive knowledge of academic subjects.  When a student has an opportunity to earn grades, he will spend more time working on his assignments and will therefore absorb more information and will achieve more comprehension.  On the other hand, students who do not have to worry about their grades won’t work very hard and will only superficially understand their subjects. My own experience as a student is a compelling example of this. During my sophomore year I had to complete a major assignment in a political science class I was taking.  According to the course syllabus, the assignment would make up about half of my total grade in the class, so I approached my work with diligence and care. I wrote an amazing speech and spent hours preparing for every possible question my classmates might think of. If the presentation had not been graded, I would not have spent so much time preparing for it.  I am sure that students all over the world today are motivated to work hard by the chance to achieve high grades from their professors.         Secondly, grades motivate students because they are a way to determine which people in a group are objectively most intelligent.  Grades are assigned in a systematic way, so they clearly demonstrate which students in a class are the best and brightest. For example, in my freshman year I took a literature class where students merely got a “pass” or “fail” at the end.  Since only a moderate amount of effort was required to pass the class, I completed my assignments and presentations quite halfheartedly. In contrast, when I took a graded class on the same subject in my junior year, I spent hours in the library researching my papers so that I could show my professors that I was intellectually superior to my classmates.  This may appear somewhat shallow, but in today’s competitive academic environment it is absolutely necessary for people to distinguish themselves.         In conclusion, I strongly believe that grades encourage students to learn.  This is because they force students to learn as much as possible, and because they give young learners a way to distinguish themselves from their peers.', \
]
topicNumList = [1, 2]
# authorList = ["Hatanaka Yu", "Ito Shunsuke", "東京 ホテイソン"]
authorList = ["8f97e799-00a2-4527-88a2-e9baa1875070"]

# タイムゾーンの生成
JST = timezone(timedelta(hours=+9), 'JST')

# GOOD, タイムゾーンを指定している．早い
createdAt = datetime.now(JST)
# createdAt = datetime.fromtimestamp(UNIX時間, JST)
# createdAt = datetime.datetime.now()

for i in range(2):
    doc_ref = db.collection('essays').document(str(uuid.uuid4().hex))
    doc_ref.set({
        # 'essay': essayList[i],
        'essay': random.choice(essayList),
        # 'createdAt' : datetime.datetime(1994, 2, 8, 1, 40, 27, 425337) ,\
        'createdAt' : createdAt, \
        'topicNum' : random.choice(topicNumList), \
        'author' : random.choice(authorList),\
        'scoreSelf': random.randrange(30)+1
    })
