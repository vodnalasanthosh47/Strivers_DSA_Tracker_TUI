#!/usr/bin/env python3
"""Entry point — run with: python main.py"""
import sys
import os

# Ensure project root is on path so imports work
sys.path.insert(0, os.path.dirname(__file__))

from app import DSATrackerApp


def main() -> None:
    app = DSATrackerApp()
    app.run()


if __name__ == "__main__":
    main()
