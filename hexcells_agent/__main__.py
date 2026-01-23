"""Module entrypoint for ``python -m hexcells_agent``."""

from __future__ import annotations

import json
import logging
from typing import Any
from uuid import uuid4

from .actuator import apply_move
from .capture import capture_screen, preprocess_image
from .cli import configure_logging, parse_args
from .parser import parse_board
from .solver import find_safe_move


def _log_event(stage: str, frame_id: str, **fields: Any) -> None:
    payload = {"stage": stage, "frame_id": frame_id, **fields}
    logging.getLogger(__name__).info(json.dumps(payload))


def main() -> None:
    """Run the Hexcells agent pipeline from the CLI."""
    options = parse_args()
    configure_logging(options.debug)

    frame_id = uuid4().hex
    _log_event("capture", frame_id, event="start", region=options.capture_region)
    image = capture_screen(region=options.capture_region)
    processed = preprocess_image(image)
    _log_event("capture", frame_id, event="complete", shape=list(processed.shape))

    _log_event(
        "parse",
        frame_id,
        event="start",
        template_dir=str(options.template_dir) if options.template_dir else None,
    )
    state = parse_board(processed, template_dir=options.template_dir)
    if options.state_out is not None:
        state.save(options.state_out)
    _log_event("parse", frame_id, event="complete", cells=len(state.cells))

    _log_event("solve", frame_id, event="start")
    move = find_safe_move(state)
    _log_event("solve", frame_id, event="complete", move_action=getattr(move, "action", None))

    _log_event("act", frame_id, event="start", dry_run=options.dry_run)
    if move is not None and not options.dry_run:
        apply_move(move)
        acted = True
    else:
        acted = False
    _log_event("act", frame_id, event="complete", acted=acted)


if __name__ == "__main__":
    main()
