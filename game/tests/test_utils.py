import uuid

import pytest

from game.utils import Action, Dir, Pos, MoveCommand


def test_pos_addition():
    pos1 = Pos(1, 2)
    pos2 = Pos(3, 4)
    direction = Dir.NORTH

    assert pos1 + pos2 == Pos(4, 6)
    assert pos1 + direction == Pos(1, 1)


def test_pos_inplace_addition():
    pos = Pos(1, 2)
    pos += Pos(3, 4)
    assert pos == Pos(4, 6)

    pos += Dir.SOUTH
    assert pos == Pos(4, 7)


def test_pos_equality():
    pos1 = Pos(1, 2)
    pos2 = Pos(1, 2)
    pos3 = Pos(3, 4)

    assert pos1 == pos2
    assert pos1 != pos3


def test_action_execute():
    action = Action()
    mushroom_id = uuid.uuid4()
    direction = Dir.SOUTH
    command = MoveCommand(id=mushroom_id, dir=direction)

    action.execute(command)

    assert action.commands_tried == 1
    assert action.mushrooms_with_commands == {mushroom_id}
    assert action.commands_to_perform == [command]


def test_action_execute_maximum_commands():
    action = Action()
    mushroom_id = uuid.uuid4()
    direction = Dir.SOUTH
    command = MoveCommand(id=mushroom_id, dir=direction)

    for _ in range(Action.MAX_COMMANDS):
        action.execute(command)

    with pytest.raises(RuntimeError):
        action.execute(command)
