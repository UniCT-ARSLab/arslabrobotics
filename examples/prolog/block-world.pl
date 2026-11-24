

% object(X) ---> X is an object
% table(X) ---> X is on the table
% upon(X,Y) ---> X is upon Y

:-
    assert(object(cube)),
    assert(object(cylinder)),
    assert(object(prism)),
    assert(object(ring)),

    assert(upon(ring, cube)),

    assert(table(cube)),
    assert(table(cylinder)),
    assert(table(prism)).

% object X is free
free(X) :- object(X), \+upon(_,X).

% put object X upon object Y
put(X, table) :- free(X), upon(X,Y), retract(upon(X, Y)), assert(table(X)).

put(X, Y) :- free(X), free(Y), table(X), retract(table(X)), assert(upon(X, Y));
             free(X), free(Y), upon(X, Z), retract(upon(X, Z)), assert(upon(X, Y)).

tower(X) :- table(X), writeln("Start"), writeln(X), find_on(X).
find_on(X) :- upon(Y, X), writeln(Y), find_on(Y).

