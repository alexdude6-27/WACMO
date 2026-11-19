"""Public WACMO calendar date handling."""

from calendar import Calendar, month_name
from datetime import datetime
from zoneinfo import ZoneInfo


MIN_YEAR = 2000
MAX_YEAR = 2100

PACIFIC = ZoneInfo("America/Los_Angeles")


def pacific_today():
    """Return today's date in Washington's local time."""
    return datetime.now(PACIFIC).date()


def build_month(year, month, today):
    """Build a Sunday-first calendar without event data."""

    if not (
        MIN_YEAR <= year <= MAX_YEAR
        and 1 <= month <= 12
    ):
        raise ValueError("Calendar month out of range")

    weeks = []

    for week in Calendar(
        firstweekday=6
    ).monthdatescalendar(year, month):
        days = []

        for day in week:
            in_month = (
                day.year == year
                and day.month == month
            )

            days.append({
                "number": day.day,
                "iso": day.isoformat(),
                "label": day.strftime(
                    "%A, %B %d, %Y"
                ),
                "in_month": in_month,
                "is_today": in_month and day == today,
            })

        weeks.append(days)

    if month == 1:
        previous = (year - 1, 12)
    else:
        previous = (year, month - 1)

    if month == 12:
        following = (year + 1, 1)
    else:
        following = (year, month + 1)

    if previous[0] < MIN_YEAR:
        previous = None

    if following[0] > MAX_YEAR:
        following = None

    return {
        "year": year,
        "month": month,
        "title": f"{month_name[month]} {year}",
        "weeks": weeks,
        "previous": previous,
        "following": following,
    }
