from graphql.core.execution import execute
from graphql.core.language.parser import parse
from graphql.core.type import GraphQLSchema, GraphQLObjectType, GraphQLField, GraphQLString


schema = GraphQLSchema(
    query=GraphQLObjectType(
        name='TestType',
        fields={
            'a': GraphQLField(GraphQLString),
            'b': GraphQLField(GraphQLString),
        }
    )
)


class Data(object):
    a = 'a'
    b = 'b'


def execute_test_query(doc):
    return execute(schema, Data, parse(doc))


def test_basic_query_works():
    result = execute_test_query('{ a, b }')
    assert not result.errors
    assert result.data == {'a': 'a', 'b': 'b'}


def test_if_true_includes_scalar():
    result = execute_test_query('{ a, b @include(if: true) }')
    assert not result.errors
    assert result.data == {'a': 'a', 'b': 'b'}


def test_if_false_omits_on_scalar():
    result = execute_test_query('{ a, b @include(if: false) }')
    assert not result.errors
    assert result.data == {'a': 'a'}


def test_skip_false_includes_scalar():
    result = execute_test_query('{ a, b @skip(if: false) }')
    assert not result.errors
    assert result.data == {'a': 'a', 'b': 'b'}


def test_skip_true_omits_scalar():
    result = execute_test_query('{ a, b @skip(if: true) }')
    assert not result.errors
    assert result.data == {'a': 'a'}


def test_if_false_omits_fragment_spread():
    q = '''
        query Q {
          a
          ...Frag @include(if: false)
        }
        fragment Frag on TestType {
          b
        }
    '''
    result = execute_test_query(q)
    assert not result.errors
    assert result.data == {'a': 'a'}


def test_if_true_includes_fragment_spread():
    q = '''
        query Q {
          a
          ...Frag @include(if: true)
        }
        fragment Frag on TestType {
          b
        }
    '''
    result = execute_test_query(q)
    assert not result.errors
    assert result.data == {'a': 'a', 'b': 'b'}


def test_skip_false_includes_fragment_spread():
    q = '''
        query Q {
          a
          ...Frag @skip(if: false)
        }
        fragment Frag on TestType {
          b
        }
    '''
    result = execute_test_query(q)
    assert not result.errors
    assert result.data == {'a': 'a', 'b': 'b'}


def test_skip_true_omits_fragment_spread():
    q = '''
        query Q {
          a
          ...Frag @skip(if: true)
        }
        fragment Frag on TestType {
          b
        }
    '''
    result = execute_test_query(q)
    assert not result.errors
    assert result.data == {'a': 'a'}


def test_if_false_omits_inline_fragment():
    q = '''
        query Q {
          a
          ... on TestType @include(if: false) {
            b
          }
        }
        fragment Frag on TestType {
          b
        }
    '''
    result = execute_test_query(q)
    assert not result.errors
    assert result.data == {'a': 'a'}


def test_if_true_includes_inline_fragment():
    q = '''
        query Q {
          a
          ... on TestType @include(if: true) {
            b
          }
        }
        fragment Frag on TestType {
          b
        }
    '''
    result = execute_test_query(q)
    assert not result.errors
    assert result.data == {'a': 'a', 'b': 'b'}


def test_skip_false_includes_inline_fragment():
    q = '''
        query Q {
          a
          ... on TestType @skip(if: false) {
            b
          }
        }
        fragment Frag on TestType {
          b
        }
    '''
    result = execute_test_query(q)
    assert not result.errors
    assert result.data == {'a': 'a', 'b': 'b'}


def test_skip_true_omits_inline_fragment():
    q = '''
        query Q {
          a
          ... on TestType @skip(if: true) {
            b
          }
        }
        fragment Frag on TestType {
          b
        }
    '''
    result = execute_test_query(q)
    assert not result.errors
    assert result.data == {'a': 'a'}


def test_if_false_omits_fragment():
    q = '''
        query Q {
          a
          ...Frag
        }
        fragment Frag on TestType @include(if: false) {
          b
        }
    '''
    result = execute_test_query(q)
    assert not result.errors
    assert result.data == {'a': 'a'}


def test_if_true_includes_fragment():
    q = '''
        query Q {
          a
          ...Frag
        }
        fragment Frag on TestType @include(if: true) {
          b
        }
    '''
    result = execute_test_query(q)
    assert not result.errors
    assert result.data == {'a': 'a', 'b': 'b'}


def test_skip_false_includes_fragment():
    q = '''
        query Q {
          a
          ...Frag
        }
        fragment Frag on TestType @skip(if: false) {
          b
        }
    '''
    result = execute_test_query(q)
    assert not result.errors
    assert result.data == {'a': 'a', 'b': 'b'}


def test_skip_true_omits_fragment():
    q = '''
        query Q {
          a
          ...Frag
        }
        fragment Frag on TestType @skip(if: true) {
          b
        }
    '''
    result = execute_test_query(q)
    assert not result.errors
    assert result.data == {'a': 'a'}
