import os

from cornice.resource import resource, view

from .restviews import BaseResource, apiroot
from ..managers.sitecontent import SiteDocumentManager

#@resource(**make_resource(path, ident='name'))
def make_resource(rpath, ident='id', cross_site=True):
    path = os.path.join(rpath, '{%s}' % ident)
    data = dict(collection_path=rpath, path=path)
    if cross_site:
        data['cors_origins'] = ('*',)
    return data

site_documents_api_path = os.path.join(apiroot(), 'sitedocuments')
@resource(**make_resource(site_documents_api_path, ident='name'))
class SiteDocumentResource(BaseResource):
    def __init__(self, request):
        super(SiteDocumentResource, self).__init__(request)
        self.mgr = SiteDocumentManager(request.dbsession)
        

    def collection_query(self):
        return self.mgr.query
    
    def collection_post(self):
        request = self.request
        name = request.json['name']
        title = request.json['title']
        description = request.json['description']
        content = request.json['content']
        # FIXME, don't hardcode markdown
        doctype = 'markdown'
        args = (name, title, description, content, doctype)
        doc = self.mgr.add_document(*args)
        response = dict(data=doc.serialize(), result='success')
        return response
    
    def get(self):
        name = self.request.matchdict['name']
        return self.serialize_object(self.mgr.getbyname(name))
    
