%
%
%

send_pos(P) :-
    py_call(ddspl:get_dds(), DDS),
    py_call(DDS:publish("position", P, 2)),
    py_call(DDS:stop).

