from nbresult import ChallengeResultTestCase


class TestSolution(ChallengeResultTestCase):

    def test_is_score_beat_baseline(self):
        self.assertLess(self.result.mae_test, 6.5)


