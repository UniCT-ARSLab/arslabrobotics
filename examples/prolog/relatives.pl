
% parent(X,Y) --> X is the the parent of Y

:-
    assert(male(james1)),
    assert(male(charles1)),
    assert(male(charles2)),
    assert(male(james2)),
    assert(male(george1)),

    assert(female(catherine)),
    assert(female(elizabeth)),
    assert(female(sophia)),

    assert(parent(james1, charles1)),
    assert(parent(james1, elizabeth)),
    assert(parent(charles1, charles2)),
    assert(parent(charles1, catherine)),
    assert(parent(charles1, james2)),
    assert(parent(elizabeth, sophia)),
    assert(parent(sophia, george1)).

% father(X,Y) --> X is the father of Y
father(X,Y) :- parent(X,Y), male(X).

% mother(X,Y) --> X is the mother of Y
mother(X,Y) :- parent(X,Y), female(X).

% X and Y are sibling
sibling(X,Y) :- parent(P, X), parent(P, Y), X \= Y.

% X is the sister of Y
sister(X,Y) :- sibling(X,Y), female(X).

% X is the brother of Y
brother(X,Y) :- sibling(X,Y), male(X).

% X is grandparent of Y
grandparent(X,Y) :- parent(X,P), parent(P,Y).

grandmother(X,Y) :- grandparent(X,Y), female(X).

grandfather(X,Y) :- grandparent(X,Y), male(X).

