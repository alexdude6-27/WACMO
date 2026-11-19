from flask import Flask, render_template


NAVIGATION = (
    ("Home", "home"),
    ("Events", "events"),
    ("Ride Flyers", "ride_flyers"),
    ("Galleries", "galleries"),
    ("Riding Areas", "riding_areas"),
    ("About", "about"),
)


PAGES = {
    "events": {
        "title": "Event Calendar",
        "description": "Find upcoming WACMO rides and events.",
        "note": (
            "The event calendar and downloadable calendar "
            "entries will be added with event management."
        ),
    },
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
        return render_template(
            "section.html", page=PAGES["events"]
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
