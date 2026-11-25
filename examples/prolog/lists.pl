
sum([], 0).
sum([H|T], S) :-
	sum(T, S1),
	S is S1 + H.

double([H], [L]) :- L is H * 2.
double([H|T], [H1|L1]) :- double(T, L1), H1 is H * 2.

