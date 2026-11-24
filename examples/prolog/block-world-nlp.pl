

:- use_module(library(readutil)).

:- assert(block(cube)),
   assert(block(cone)),
   assert(block(prism)),
   assert(block(cylinder)),

   assert(table(cube)),
   assert(table(cone)),
   assert(table(prism)),
   assert(table(cylinder)),

   assert(pos(cube, -1.0)),
   assert(pos(cylinder, -0.3)),
   assert(pos(cone, 0.3)),
   assert(pos(prism, 1.0)).


command(pick(Object)) -->
    pick_verb, article, obj(Object);
    pick_verb, obj(Object).

command(put(Object)) -->
    put_verb, article, obj(Object);
    put_verb, obj(Object).

pick_verb --> [get] ; [pick] ; [grab].
put_verb --> [put] ; [drop].

article --> [the].

obj(cube) --> [cube].
obj(prism) --> [prism].
obj(cone) --> [cone].
obj(cylinder) --> [cylinder].


interpret_phrase(StringPhrase, LogicCommand) :-
    string_lower(StringPhrase, Lower),
    split_string(Lower, " ", ".,!?", StringList),
    maplist(atom_string, Words, StringList),
    phrase(command(LogicCommand), Words).



pick(Object) :-
    % the object is on the table
    block(Object), free(Object), table(Object), pos(Object, X), !,
    py_call(ddspl:publish("command", [ pick, Object] )),
    assert(own(Object)), retract(table(Object)),
    retract(pos(Object, X)), assert(free_pos(X));

    % the object is already owned by the robot
    block(Object), free(Object), own(Object),
    format("I already own ~w~n", [Object]).



put(Object) :-
    block(Object), free(Object), table(Object),
    format("The ~w is already on the table~n", [Object]);

    block(Object), own(Object), free_pos(X), !,
    py_call(ddspl:publish("command", [ put, Object, X, 0.1] )),
    assert(table(Object)), retract(own(Object)),
    assert(pos(Object, X)), retract(free_pos(X)).


start :-
    py_call(ddspl:create()).

ask :-
    repeat,
    write('Insert command (quit to exit): '),
    flush_output,
    read_line_to_string(user_input, Phrase),
    ( Phrase == "quit" -> ! ; do(Phrase), fail).

do(Phrase) :-
    interpret_phrase(Phrase, Command),
    format('The Command is: "~w"~n', [Command]),
    Command.
