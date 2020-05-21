from operator import and_, or_

from toydb.table import reduce_booleans_using_conjunctions


class TestEvaluator:
    def test_reduce(self):
        assert reduce_booleans_using_conjunctions(conditions=[True, False], conjunctions=[and_]) is False
        assert reduce_booleans_using_conjunctions(conditions=[True, False], conjunctions=[or_]) is True
        assert reduce_booleans_using_conjunctions(conditions=[False, False, True], conjunctions=[and_, or_]) is True
