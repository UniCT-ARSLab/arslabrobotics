

:- use_module(library(readutil)).


command(pick(Object)) -->
    pick_verb, article, obj(Object);
    pick_verb, obj(Object).

pick_verb --> [get] ; [pick] ; [grab].

article --> [the] ; [a].

obj(cube) --> [cube].
obj(prism) --> [prism].


pick(Object) :- format('Picking ~w~n', [Object]).

interpret_phrase(StringPhrase, LogicCommand) :-
    string_lower(StringPhrase, Lower),
    split_string(Lower, " ", ".,!?", StringList),
    maplist(atom_string, Words, StringList),
    phrase(command(LogicCommand), Words).


ask :-
    write('Insert Command: '),
    flush_output,
    read_line_to_string(user_input, Phrase),
    execute(Phrase).

execute("quit").
execute(Phrase) :-
    interpret_phrase(Phrase, Command),
    format('The Command is: "~w"~n', [Command]),
    Command,
    ask.
