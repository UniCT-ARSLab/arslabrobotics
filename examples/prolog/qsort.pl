

qsort([], []) :- ! .
qsort([X], [X]) :- ! .
qsort([X|T], L) :-
    findall(A, (member(A,T), A < X), Left),
    findall(A, (member(A,T), A > X), Right),
    qsort(Left, LeftSorted),
    qsort(Right, RightSorted),
    append(LeftSorted, [X], L1),
    append(L1, RightSorted, L).
