from flask import Flask, abort, render_template, request

from .calendar import build_month, pacific_today
from .events_archive import load_archived_schedule


NAVIGATION = (
    ("Home", "home"),
    ("What is CMO?", "what_is_cmo"),
    ("CMO History", "cmo_history"),
    ("Schedule of Events", "events"),
    ("Flyers (Rides & Invites)", "ride_flyers"),
    ("Photo Gallery", "galleries"),
    ("Maps", "riding_areas"),
    ("Forms", "forms"),
    ("Links", "links"),
)

NAV_GROUPS = (
    ("About CMO", NAVIGATION[1:3]),
    ("Events", NAVIGATION[3:5]),
    ("Explore", NAVIGATION[5:7]),
    ("Resources", NAVIGATION[7:9]),
)


PAGES = {
    "what_is_cmo": {
        "title": "What is CMO?",
        "description": (
            "Learn about Competitive Mounted Orienteering."
        ),
        "note": (
            "The original WACMO information will be "
            "transferred here."
        ),
    },
    "cmo_history": {
        "title": "CMO History",
        "description": "The history of mounted orienteering.",
        "note": (
            "Historical WACMO materials will be added here."
        ),
    },
    "forms": {
        "title": "Forms",
        "description": "WACMO forms and documents.",
        "note": (
            "Approved downloadable forms will appear here."
        ),
    },
    "links": {
        "title": "Links",
        "description": "Helpful mounted orienteering resources.",
        "note": (
            "Approved links will be added here."
        ),
    },
    "ride_flyers": {
        "title": "Flyers (Rides & Invites)",
        "description": "Flyers for rides, past and present.",
        "note": (
            "Flyer uploads, searching, and automatic "
            "archives will be added here."
        ),
    },
    "galleries": {
        "title": "Photo Gallery",
        "description": "Memories from WACMO riding adventures.",
        "note": (
            "Approved photographs will be organized into "
            "albums with easy volunteer uploads."
        ),
    },
    "riding_areas": {
        "title": "Maps",
        "description": "Discover the landscapes where we ride.",
        "note": (
            "General riding locations and approved historical "
            "maps will be shared without revealing upcoming courses."
        ),
    },
    "about": {
        "title": "About WACMO",
        "description": (
            "Washington Association of Competitive "
            "Mounted Orienteering."
        ),
        "note": (
            "Organization details and contact information "
            "will be added when approved."
        ),
    },
}


def create_app():
    app = Flask(__name__)

    @app.context_processor
    def site_navigation():
        return {
            "navigation": NAVIGATION,
            "nav_groups": [
                {
                    "label": label,
                    "links": links,
                    "active": any(
                        request.endpoint == endpoint
                        for _, endpoint in links
                    ),
                }
                for label, links in NAV_GROUPS
            ],
        }

    @app.get("/")
    def home():
        return render_template("index.html")

    @app.get("/events")
    def events():
        today = pacific_today()

        year_text = request.args.get("year")
        month_text = request.args.get("month")

        if year_text is None and month_text is None:
            year, month = today.year, today.month
        else:
            if year_text is None or month_text is None:
                abort(400)

            if not (
                len(year_text) == 4
                and year_text.isascii()
                and year_text.isdigit()
                and 1 <= len(month_text) <= 2
                and month_text.isascii()
                and month_text.isdigit()
            ):
                abort(400)

            year = int(year_text)
            month = int(month_text)

        try:
            calendar_view = build_month(year, month, today)
        except ValueError:
            abort(400)

        days_in_month = [
            day["iso"]
            for week in calendar_view["weeks"]
            for day in week
            if day["in_month"]
        ]
        first_day, last_day = days_in_month[0], days_in_month[-1]

        month_events = [
            event for event in load_archived_schedule()
            if event["start_date"] <= last_day
            and event["end_date"] >= first_day
        ]

        for week in calendar_view["weeks"]:
            for day in week:
                day["events"] = [
                    event for event in month_events
                    if day["in_month"]
                    and event["start_date"] <= day["iso"] <= event["end_date"]
                ]

        archive_year_text = request.args.get("archive_year")
        archive_year = None
        older_years = list(
            range(today.year - 3, 2010, -1)
        )

        if archive_year_text is not None:
            if not (
                len(archive_year_text) == 4
                and archive_year_text.isascii()
                and archive_year_text.isdigit()
                and int(archive_year_text) in older_years
            ):
                abort(400)
            archive_year = int(archive_year_text)

        recent_years = range(today.year, today.year - 3, -1)

        recent_archives = [
            {
                "year": year_value,
                "events": sorted(
                    (
                        event
                        for event in load_archived_schedule()
                        if int(event["start_date"][:4]) == year_value
                    ),
                    key=lambda event: (
                        event["start_date"],
                        event["id"],
                    ),
                    reverse=True,
                ),
            }
            for year_value in recent_years
        ]

        older_events = []
        if archive_year is not None:
            older_events = sorted(
                (
                    event
                    for event in load_archived_schedule()
                    if int(event["start_date"][:4]) == archive_year
                ),
                key=lambda event: (
                    event["start_date"],
                    event["id"],
                ),
                reverse=True,
            )

        return render_template(
            "events.html",
            calendar=calendar_view,
            month_events=month_events,
            recent_archives=recent_archives,
            older_years=older_years,
            archive_year=archive_year,
            older_events=older_events,
        )

    @app.get("/what-is-cmo")
    def what_is_cmo():
        return render_template("what_is_cmo.html")

    @app.get("/cmo-history")
    def cmo_history():
        return render_template("cmo_history.html")

    @app.get("/forms")
    def forms():
        return render_template("forms.html")

    @app.get("/links")
    def links():
        return render_template("links.html")

    @app.get("/ride-flyers")
    def ride_flyers():
        return render_template("ride_flyers.html")

    @app.get("/galleries")
    def galleries():
        return render_template("galleries.html")

    @app.get("/riding-areas")
    def riding_areas():
        return render_template("riding_areas.html")

    @app.get("/about")
    def about():
        return render_template(
            "section.html", page=PAGES["about"]
        )

    return app
