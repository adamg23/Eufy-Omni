"""Import the cloud client.

In a deployed copy the library is vendored at ./eufy_omni_cloud (see tools/deploy.ps1);
in the development tree it is importable from the repository root.
"""

from __future__ import annotations

try:
    from .eufy_omni_cloud import commands  # type: ignore[attr-defined]
    from .eufy_omni_cloud.account import EufyAccount, RobotVacuum  # type: ignore[attr-defined]
    from .eufy_omni_cloud.exceptions import EufyAuthError, EufyCloudError, EufyConnectionError  # type: ignore[attr-defined]
    from .eufy_omni_cloud.maprender import render_png  # type: ignore[attr-defined]
    from .eufy_omni_cloud.mapstream import RobotMap  # type: ignore[attr-defined]
    from .eufy_omni_cloud.state import (  # type: ignore[attr-defined]
        CLEAN_EXTENTS,
        CLEAN_TYPES,
        CONSUMABLES,
        FAN_SPEEDS,
        MOP_LEVELS,
        Activity,
        DockActivity,
        VacuumSnapshot,
    )
except ImportError:  # development checkout
    from eufy_omni_cloud import commands
    from eufy_omni_cloud.account import EufyAccount, RobotVacuum
    from eufy_omni_cloud.exceptions import EufyAuthError, EufyCloudError, EufyConnectionError
    from eufy_omni_cloud.maprender import render_png
    from eufy_omni_cloud.mapstream import RobotMap
    from eufy_omni_cloud.state import (
        CLEAN_EXTENTS,
        CLEAN_TYPES,
        CONSUMABLES,
        FAN_SPEEDS,
        MOP_LEVELS,
        Activity,
        DockActivity,
        VacuumSnapshot,
    )

__all__ = [
    "CLEAN_EXTENTS",
    "CLEAN_TYPES",
    "CONSUMABLES",
    "FAN_SPEEDS",
    "MOP_LEVELS",
    "Activity",
    "DockActivity",
    "EufyAccount",
    "EufyAuthError",
    "EufyCloudError",
    "EufyConnectionError",
    "RobotMap",
    "RobotVacuum",
    "VacuumSnapshot",
    "commands",
    "render_png",
]
