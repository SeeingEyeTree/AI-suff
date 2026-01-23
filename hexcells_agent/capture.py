"""Screen capture and preprocessing utilities for Hexcells automation."""

from __future__ import annotations

from typing import Optional, Tuple

import cv2
import numpy as np
import pyautogui


def capture_screen(region: Optional[Tuple[int, int, int, int]] = None) -> np.ndarray:
    """Capture the screen (or region) and return a BGR image.

    Args:
        region: Optional (left, top, width, height) tuple to crop capture.

    Returns:
        A NumPy array in BGR color space representing the captured screen.
    """
    screenshot = pyautogui.screenshot(region=region)
    image = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
    return image


def preprocess_image(image: np.ndarray) -> np.ndarray:
    """Preprocess a captured image for board parsing.

    Args:
        image: BGR image array from ``capture_screen``.

    Returns:
        A grayscale, blurred image optimized for edge/shape detection.
    """
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    return blurred
