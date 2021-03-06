from peewee import *

db = SqliteDatabase('databases/database.db')
db.connect()


class Question(Model):
    thread_id = IntegerField()
    judge = CharField()
    problem_name = CharField()
    problem = CharField()

    def value(self):
        print(self.id, self.thread_id, self.judge,
              self.problem_name, self.problem)

    class Meta:
        database = db


db.create_tables([Question])


def insert_thread(*, thread_id, judge, problem_name, problem):
    Question.create(thread_id=thread_id, judge=judge,
                    problem_name=problem_name, problem=problem).save()


def select_questions(*, thread_id=None, problem_name=None, problem=None):
    exp = True

    if thread_id:
        exp = exp & (Question.thread_id == thread_id)
    if problem_name:
        exp = exp & (Question.problem_name == problem_name)
    if problem:
        exp = exp & (Question.problem == problem)

    return Question.select().where(exp)


def related_questions(*queries):
    def match(query, question):
        query = query.lower()
        if query in question.problem_name.lower():
            return True
        if query in question.problem.lower():
            return True
        return False

    return [question for question in Question.select() if any(match(query, question) for query in queries if query)]


class Topic(Model):
    topic_name = CharField()
    guild_id = IntegerField()
    channel_id = IntegerField()

    def value(self):
        print(self.id, self.topic_name, self.guild_id, self.channel_id)

    class Meta:
        database = db


db.create_tables([Topic])


def insert_topic(*, topic_name, guild_id, channel_id):
    Topic.create(topic_name=topic_name, guild_id=guild_id,
                 channel_id=channel_id).save()


def select_topics(*, topic_name=None, guild_id=None, channel_id=None):
    exp = True

    if topic_name:
        exp = exp & (Topic.topic_name == topic_name)
    if guild_id:
        exp = exp & (Topic.guild_id == guild_id)
    if channel_id:
        exp = exp & (Topic.channel_id == channel_id)

    return Topic.select().where(exp)


def update_topic_information(topic_name, guild_id, channel_id):
    updated_topic_list = select_topics(
        topic_name=topic_name, guild_id=guild_id)

    if len(updated_topic_list) > 1:
        print("Failed")
        return
    if len(updated_topic_list) == 0:
        print("Failed")
        return

    updated_topic = updated_topic_list[0]
    updated_topic.channel_id = channel_id
    updated_topic.save()


class GuildInformation(Model):
    guild_id = IntegerField()
    default_channel_id = IntegerField()

    def value(self):
        print(self.id, self.guild_id, self.default_channel_id)

    class Meta:
        database = db


db.create_tables([GuildInformation])


def insert_guild(*, guild_id, default_channel_id):
    GuildInformation.create(
        guild_id=guild_id, default_channel_id=default_channel_id).save()


def select_guilds(*, guild_id=None, default_channel_id=None):
    exp = True
    if guild_id:
        exp = exp & (GuildInformation.guild_id == guild_id)
    if default_channel_id:
        exp = exp & (GuildInformation.default_channel_id == default_channel_id)

    return GuildInformation.select().where(exp)


def update_guild_information(guild_id, channel_id):
    updated_guild_list = select_guilds(guild_id=guild_id)

    if len(updated_guild_list) > 1:
        print("Failed")
        return
    if len(updated_guild_list) == 0:
        print("Failed")
        return

    updated_guild = updated_guild_list[0]
    updated_guild.default_channel_id = channel_id
    updated_guild.save()


def database_information():
    for question in Question.select():
        print(question.value())
    for topic in Topic.select():
        print(topic.value())
    for guild_information in GuildInformation.select():
        print(guild_information.value())
