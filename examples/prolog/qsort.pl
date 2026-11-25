

qsort([], []) :- ! .
qsort([X], [X]) :- ! .
qsort([X|T], L) :-
    findall(A, (member(A,T), A < X), Left),
    findall(A, (member(A,T), A >= X), Right),
    qsort(Left, LeftSorted),
    qsort(Right, RightSorted),
    append(LeftSorted, [X], L1),
    append(L1, RightSorted, L).
    
 % [10,23,6,10,3,5,6]
 %  sort([6,3,5,6]) + [10] + sort([10,23])
