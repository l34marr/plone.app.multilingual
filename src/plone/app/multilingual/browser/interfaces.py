# -*- coding: utf-8 -*-
from Acquisition import aq_parent
from plone.app.multilingual import _
from plone.app.multilingual.browser.vocabularies import deletable_languages
from plone.app.multilingual.browser.vocabularies import untranslated_languages
from plone.app.z3cform.widget import RelatedItemsFieldWidget
from plone.autoform import directives
from plone.autoform.directives import widget
from plone.autoform.interfaces import IFormFieldProvider
from plone.supermodel import model
from Products.CMFPlone.interfaces import IPloneSiteRoot
from z3c.relationfield.schema import RelationChoice
from zope import interface
from zope import schema
from zope.browsermenu.interfaces import IBrowserMenu
from zope.browsermenu.interfaces import IBrowserSubMenuItem
from zope.component.hooks import getSite


class IMultilingualLayer(interface.Interface):
    """ browser layer """


class ITranslateSubMenuItem(IBrowserSubMenuItem):
    """The menu item linking to the translate menu.
    """


class ITranslateMenu(IBrowserMenu):
    """The translate menu.
    """


class ICreateTranslation(interface.Interface):

    language = schema.Choice(
        title=_(u"title_language", default=u"Language"),
        source=untranslated_languages,
    )


class IUpdateLanguage(interface.Interface):

    language = schema.Choice(
        title=_(u"title_available_languages", default=u"Available languages"),
        description=_(
            u"description_update_language",
            default=u"Untranslated languages from the current content"
        ),
        source=untranslated_languages,
        required=True,
    )


def make_relation_root_path(context):
    ctx = getSite()
    if not IPloneSiteRoot.providedBy(ctx):
        ctx = aq_parent(ctx)
    return u'/'.join(ctx.getPhysicalPath())


class IAddTranslation(model.Schema):

    language = schema.Choice(
        title=_(u"title_language", default=u"Language"),
        source=untranslated_languages,
        required=True,
    )
    content = RelationChoice(
        title=_(u"content"),
        vocabulary="plone.app.multilingual.RootCatalog",
        required=True,
    )

    widget(
        'content',
        RelatedItemsFieldWidget,
        pattern_options={
            'basePath': make_relation_root_path,
        }
    )


class IRemoveTranslation(model.Schema):

    languages = schema.List(
        title=_(u"title_languages"),
        value_type=schema.Choice(
            title=_(u"title_language", default=u"Language"),
            source=deletable_languages,
        ),
        required=True,
    )
    directives.widget(languages='z3c.form.browser.select.SelectFieldWidget')

interface.alsoProvides(IUpdateLanguage, IFormFieldProvider)
interface.alsoProvides(IAddTranslation, IFormFieldProvider)
interface.alsoProvides(IRemoveTranslation, IFormFieldProvider)
