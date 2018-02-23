from elasticsearch_dsl import DocType, Integer, Text
from elasticsearch import NotFoundError


class Model(object):
    @classmethod
    def safe_get(cls, id):
        try:
            obj = cls.get(id=id)
        except NotFoundError:
            obj = None
        return obj


class Faculty(DocType, Model):
    faculty_id = Integer(required=True)
    name = Text(required=True)
    email = Text(required=True)
    department = Text()

    google_scholar = Text()
    orc_id = Text()
    sciverse_id = Text()
    research_id = Text()

    user_keywords = Text()

    class Meta:
        index = "faculty"

    def __str__(self):
        return "<Faculty ID:{} Name: {} Email: {}".format(self.faculty_id, self.name, self.email)


class Grant(DocType):
    faculty_id = Integer(required=True)
    grant_id = Integer()                    # grant_id is the provided id in the json data dump. May not be useful.

    application_title = Text()
    application_area_group = Text()
    application_area = Text()
    research_subject = Text()

    co_applicants = Integer()

    class Meta:
        index = "grants"


class Publication(DocType):
    publication_id = Integer(required=True)
    authors = Integer(required=True)
    title = Text()
    type = Text()
    url = Text()
    data = Text()
    
    class Meta:
        index = "publications"


def initialize_models():
    """Initializes the mappings of all models in ElasticSearch. A connection should have already been established."""
    Faculty.init()
    Grant.init()
    Publication.init()


# if __name__ == "__main__":
#     from elasticsearch_dsl.connections import connections
#     connections.create_connection(hosts=["localhost"])

#     Faculty.init()

#     prof = Faculty(meta={'id': 42}, name="Garry Bullock", email="gbullock@ualberta.ca", faculty_id=42)
#     prof.save()

#     saved_prof = Faculty.get(id=42)
#     print(saved_prof.name)

#     print(connections.get_connection().cluster.health())