"""Phase 16 Canonical Backlog Core Data Aggregator"""

from scripts.backlog.backlog_data_part1 import EPICS, BACKLOG_FEATURES
from scripts.backlog.backlog_data_part2 import USER_STORIES
from scripts.backlog.backlog_data_part3 import TASKS
from scripts.backlog.backlog_data_part4 import MICRO_TASKS
from scripts.backlog.backlog_data_part5 import BACKLOG_DEPENDENCIES, BACKLOG_TESTS
from scripts.backlog.backlog_data_part6 import BACKLOG_RISKS, RELEASE_MAPPINGS, SPRINT_MAPPINGS

__all__ = [
    "EPICS",
    "BACKLOG_FEATURES",
    "USER_STORIES",
    "TASKS",
    "MICRO_TASKS",
    "BACKLOG_DEPENDENCIES",
    "BACKLOG_TESTS",
    "BACKLOG_RISKS",
    "RELEASE_MAPPINGS",
    "SPRINT_MAPPINGS",
]
