
from __future__ import annotations

from blindman.game.object.event_manager import EventManager, Event

from attrs import define, field


@define(eq=False)
class Timeline:
    manager: EventManager
    moment: int = field(init=False, default=0)

    def append_event(self, *events: Event) -> None:
        for event in events:
            self.manager.append_event(self.moment, event)

    def wait(self, delta: int) -> None:
        self.moment += delta