from mongoengine import Document, EmbeddedDocument, fields


class ElementType(Document):
	name = fields.StringField(required = True)
	description = fields.StringField( required = True)


class Locator(Document):
	name = fields.StringField(required = True)
	description = fields.StringField( required = True)


class Action(Document):
	name = fields.StringField(required = True)
	actiontype = fields.StringField(required = True)


class Page(Document):
	name = fields.StringField(required = True)
	description = fields.StringField( required = True)


class Element(Document):
	name = fields.StringField(required = True)
	description = fields.StringField( required = True)
	elementtype = fields.StringField(required = True)
	locator = fields.StringField( required = True)
	identification = fields.StringField(required = True)
	pageid = fields.StringField(required = True)


class TestCase(Document):
	name = fields.StringField(required = True)
	description = fields.StringField(required = True)


class Component(Document):
	name = fields.StringField(required = True)
	description = fields.StringField(required = True)
	testcaseid = fields.StringField(required = True)


class Step(Document):
	name = fields.StringField(required = True)
	componentid = fields.StringField( required = True)
	page = fields.StringField( required = True)
	element = fields.StringField(required = True)
	action = fields.StringField(required = True)
	order = fields.StringField(required = True)
	data = fields.StringField(required = False)	
