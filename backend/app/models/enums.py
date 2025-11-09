from __future__ import annotations

import enum


class EquipmentStatus(enum.StrEnum):
    WORKING = "WORKING"
    UNDER_REPAIR = "UNDER_REPAIR"
    EXPIRED = "EXPIRED"
    DECOMMISSIONED = "DECOMMISSIONED"


class IssueType(enum.StrEnum):
    TECHNICAL = "TECHNICAL"
    MECHANICAL = "MECHANICAL"
    ELECTRICAL = "ELECTRICAL"
    USER_OPERATION = "USER_OPERATION"


class IssueStatus(enum.StrEnum):
    OPEN = "OPEN"
    IN_PROGRESS = "IN_PROGRESS"
    RESOLVED = "RESOLVED"
    CLOSED = "CLOSED"


class UserRole(enum.StrEnum):
    ADMIN = "ADMIN"
    TECHNICIAN = "TECHNICIAN"
    VIEWER = "VIEWER"
