from five import grok
from seantis.people.interfaces import ISeantisPeopleSpecific


class BaseView(grok.View):

    grok.baseclass()
    grok.layer(ISeantisPeopleSpecific)
