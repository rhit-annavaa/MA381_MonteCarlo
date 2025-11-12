def pythag_expectation(rs, ra, n=1.83):
    return (rs ** n) / ((rs ** n) + (ra ** n))
print(pythag_expectation(643, 649))