from google.appengine.ext import ndb


class Account(ndb.Model):
    username = ndb.StringProperty()
    userid = ndb.IntegerProperty()
    email = ndb.StringProperty()


class Address(ndb.Model):
    type = ndb.StringProperty()  # E.g., 'home', 'work'
    street = ndb.StringProperty()
    city = ndb.StringProperty()


class Contact(ndb.Model):
    name = ndb.StringProperty()
    addresses = ndb.StructuredProperty(Address, repeated=True)


class Article(ndb.Model):
    title = ndb.StringProperty()
    stars = ndb.IntegerProperty()
    tags = ndb.StringProperty(repeated=True)


class ArticleWithDifferentDatastoreName(ndb.Model):
    title = ndb.StringProperty('t')


class Employee(ndb.Model):
    full_name = ndb.StringProperty('n')
    retirement_age = ndb.IntegerProperty('r')


class Manager(ndb.Model):
    pass


class FlexEmployee(ndb.Expando):
    name = ndb.StringProperty()
    age = ndb.IntegerProperty()


class Bar(ndb.Model):
    pass


class Message(ndb.Model):
    content = ndb.StringProperty()
    userid = ndb.IntegerProperty()