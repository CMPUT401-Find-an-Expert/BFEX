from elasticsearch_dsl.search import Q
from bfex.components.search_engine.stack import Stack

bool_values = ['AND', 'OR']


class QueryBuilder(object):
    """Creates ElasticSearch queries out of postfix ordered lists."""

    def build(self, pf_query, search_field="keywords"):
        """Builds a boolean query for elasticsearch from a postfix ordered lists.

        :param pf_query: Postfix ordered query list
        :param search_field: The field to search in the elastic search objects.
            Defaults to 'keywords'. Allows creation of queries for other objects.
        :return: Elasticsearch Q object"""
        stack = Stack()

        if len(pf_query) == 1:
            stack.push(Q('match', **{search_field: pf_query[0][1]}))

        for token in pf_query:
            if token in bool_values:
                q1 = stack.pop()
                q2 = stack.pop()

                result = q1 & q2 if token == 'AND' else q1 | q2
                stack.push(result)
            else:
                q = None
                if token[0] == 'KEYWORD':
                    q = Q('match', **{search_field: token[1]})
                else:
                    q = Q('match_phrase', **{search_field: " ".join(token[1])})
                stack.push(q)

        return stack.pop()
