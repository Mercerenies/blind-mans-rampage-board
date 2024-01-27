
from __future__ import annotations

from blindman.game.object.events import EventManager, Event

from attrs import define, field

from typing import Protocol


@define(eq=False)
class Timeline:
    """A Timeline is a write-only register of events. This class is a
    convenience implemented on top of EventManager for writing events
    in a procedural way.

    A Timeline starts at moment 0, and the moment can be advanced with
    the wait() method. When an event is scheduled with append_event(),
    the event is scheduled for the timeline's current moment.

    """

    manager: EventManager
    moment: int = field(init=False, default=0)

    def append_event(self, *events: Event) -> None:
        """Schedule an event for the timeline's current moment."""
        for event in events:
            self.manager.append_event(self.moment, event)

    def wait(self, delta: int) -> None:
        """Advance the timeline's moment."""
        self.moment += delta


class TimelineLike(Protocol):
    """Protocol for the minimal interface satisfied by the Timeline
    class.

    """

    def append_event(self, *events: Event) -> None:
        ...

    def wait(self, delta: int) -> None:
        ...
