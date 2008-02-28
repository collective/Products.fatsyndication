# Five imports
from Products.Five import BrowserView
from Products.Five.browser.pagetemplatefile \
    import ZopeTwoPageTemplateFile as PageTemplateFile

# Zope3 imports
from zope.component import getMultiAdapter

# basesyndication imports
from Products.basesyndication.interfaces import IFeed


class FeedView(BrowserView):
    """Provides the various feed views for the IFeed interface.
    """

    def __init__(self, context, request):
        response = request.RESPONSE
        encoding = context.getEncoding()
        # TODO: Atom wants a different content type (at least I
        # thought so).
        header = 'text/xml; charset=%s' % encoding
        response.setHeader('Content-Type', header)
        modified = context.getModifiedDate()
        response.setHeader('Last-Modified', modified.toZone('GMT').rfc822())
        return super(FeedView, self).__init__(context, request)

    atom  = PageTemplateFile('../../basesyndication/browser/atom.xml.pt')
    rss   = PageTemplateFile('../../basesyndication/browser/rss.xml.pt')
    rdf   = PageTemplateFile('../../basesyndication/browser/feed.rdf.pt')
    rdf11 = PageTemplateFile('../../basesyndication/browser/feed11.rdf.pt')
    itunes = PageTemplateFile('../../basesyndication/browser/itunes.xml.pt')

class GenericFeedView(BrowserView):
    """Adapts its context to IFeed, then looks up the appropriate view to
    render the actual feed for the resultant IFeed.

    You should declare an adapter from your class' interface to IFeed, then
    use this view for your class' interface in order to get feeds for it.
    """

    def getFeed(self):
        # This first test may be superfluous.  The motivation is that we
        # don't want the returned IFeed to be wrapped in itself if 'self'
        # already implements IFeed.
        if IFeed.providedBy(self):
            return self
        # Must have an acquisition context in order to play properly
        # with zope
        feed = IFeed(self.context).__of__(self.context)
        return feed

    def atom(self):
        """ """
        feed = self.getFeed()
        view = getMultiAdapter((feed, self.request), name='atom.xml')
        return view()

    def rdf(self):
        """ """
        feed = self.getFeed()
        view = getMultiAdapter((feed, self.request), name='feed.rdf')
        return view()

    def rdf11(self):
        """ """
        feed = self.getFeed()
        view = getMultiAdapter((feed, self.request), name='feed11.rdf')
        return view()
   
    def itunes(self):
        """ """
        feed = self.getFeed()
        view = getMultiAdapter((feed, self.request), name='itunes.xml')
        return view()
     
    def rss(self):
        """ """
        feed = self.getFeed()
        view = getMultiAdapter((feed, self.request), name='rss.xml')
        return view()

