from nbresult import ChallengeResultTestCase


class TestSolution(ChallengeResultTestCase):
    def test_cv_results(self):
        self.assertEqual(self.result.scoring, "precision")
        self.assertGreaterEqual(self.result.cv, 2, msg = "You should explicitly use at least 2 folds for cross-validation (i.e. pass cv=2 to GridSearchCV)")
        self.assertGreaterEqual(len(self.result.mean_test_score), 5)
