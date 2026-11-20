from flask import Flask, abort, render_template, request

from .calendar import build_month, pacific_today


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
