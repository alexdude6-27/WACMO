from flask import Flask, abort, render_template, request

from .calendar import build_month, pacific_today


NAVIGATION = (
    ("Home", "home"),
    ("Events", "events"),
    ("Ride Flyers", "ride_flyers"),
    ("Galleries", "galleries"),
    ("Riding Areas", "riding_areas"),
    ("About", "about"),
)


PAGES = {
    "ride_flyers": {
        "title": "Ride Flyers",
        "description": "Flyers for rides, past and present.",
        "note": (
            "Flyer uploads, searching, and automatic "
            "archives will be added here."
        ),
    },
    "galleries": {
        "title": "Photo Galleries",
        "description": "Memories from WACMO riding adventures.",
        "note": (
            "Approved photographs will be organized into "
            "albums with easy volunteer uploads."
        ),
    },
    "riding_areas": {
        "title": "Riding Areas",
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
        return {"navigation": NAVIGATION}

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

        return render_template(
            "events.html",
            calendar=calendar_view,
        )

    @app.get("/ride-flyers")
    def ride_flyers():
        return render_template(
            "section.html", page=PAGES["ride_flyers"]
        )

    @app.get("/galleries")
    def galleries():
        return render_template(
            "section.html", page=PAGES["galleries"]
        )

    @app.get("/riding-areas")
    def riding_areas():
        return render_template(
            "section.html", page=PAGES["riding_areas"]
        )

    @app.get("/about")
    def about():
        return render_template(
            "section.html", page=PAGES["about"]
        )

    return app
