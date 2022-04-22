from re import X
from discord import Guild
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

class Topic(Model):
    topic_name = CharField()
    guild_id = IntegerField()
    channel_id = IntegerField()
    
    class Meta:
        database = db

class GuildList(Model):
    guild_id = IntegerField()
    default_channel_id = IntegerField()

    class Meta:
        database = db

db.connect()
db.create_tables([GuildList])
db.create_tables([Topic])
db.create_tables([Question])

def insert_thread(*, thread_id, judge, problem_name, problem_id):
    Question.create(thread_id=thread_id, judge=judge,
                    problem_name=problem_name, problem_id=problem_id).save()

def select_questions(*, thread_id=None, problem_name=None, problem_id=None):
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

def insert_topic(*, topic_name, guild_id, channel_id):
    Topic.create(topic_name = topic_name, guild_id = guild_id, channel_id = channel_id).save()

def select_topics(*, topic_name = None, guild_id = None, channel_id = None):
    exp = True

    if topic_name:
        exp = exp & (Topic.topic_name == topic_name)
    if guild_id:
        exp = exp & (Topic.guild_id == guild_id)
    if channel_id:
        exp = exp & (Topic.channel_id == channel_id)
    
    return Topic.select().where(exp)

def insert_guild(*, guild_id, default_channel_id):
    GuildList.create(guild_id = guild_id, default_channel_id = default_channel_id).save()

def select_guide