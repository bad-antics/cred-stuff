from cred_stuff.core import CredentialDefender
d = CredentialDefender(max_attempts=5, lockout_time=900)
for i in range(6):
    r = d.record_attempt("admin", "1.2.3.4")
    print(f"Attempt {i+1}: {r}")
