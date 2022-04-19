from re import X
from peewee import *
import peewee

db = SqliteDatabase('database.db')


class Question(Model):
    thread_id = IntegerField()
    judge = CharField()
    problem_name = CharField()
    problem_id = CharField()

    class Meta:
        database = db


db.connect()
db.create_tables([Question])


def insert(*, thread_id, judge, problem_name, problem_id):
    Question.create(thread_id=thread_id, judge=judge,
                    problem_name=problem_name, problem_id=problem_id).save()


def select(*, thread_id=None, problem_name=None, problem_id=None):
    exp = True

    if thread_id:
        exp = exp & (Question.thread_id == thread_id)
    if problem_name:
        exp = exp & (Question.problem_name == problem_name)
    if problem_id:
        exp = exp & (Question.problem_id == problem_id)

    return Question.select().where(exp)


def related_questions(query):

    def match(query, question):
        query = query.lower()
        if query in question.problem_name.lower():
            return True
        if query in question.problem_id.lower():
            return True
        return False

    return [question for question in Question.select() if match(query, question)]
