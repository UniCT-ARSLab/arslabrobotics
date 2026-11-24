
sgn(0,S) :- S is 0.
sgn(N,S) :- (N > 0, S is 1);(N < 0, S is -1).

