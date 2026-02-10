import unittest, sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
from cred_stuff.core import CredentialDefender

class TestDefender(unittest.TestCase):
    def test_lockout(self):
        d = CredentialDefender(max_attempts=3, lockout_time=60)
        for i in range(3):
            d.record_attempt("user1", "1.2.3.4")
        self.assertTrue(d.is_locked("user1"))
    def test_success_resets(self):
        d = CredentialDefender(max_attempts=3)
        d.record_attempt("user1", "1.2.3.4")
        d.record_attempt("user1", "1.2.3.4")
        d.record_attempt("user1", "1.2.3.4", success=True)
        self.assertFalse(d.is_locked("user1"))

if __name__ == "__main__": unittest.main()
