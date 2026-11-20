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

    @app.context_processor
    def inject_event_flyers():
        from .event_flyers import load_event_flyers

        return {
            "event_flyers": load_event_flyers(),
        }

    @app.get("/events/<event_id>")
    def event_detail(event_id):
        event = next(
            (
                record
                for record in load_archived_schedule()
                if record["id"] == event_id
            ),
            None,
        )

        if event is None:
            abort(404)

        from .photo_albums import albums_for_event

        return render_template(
            "event_detail.html",
            event=event,
            event_photo_albums=albums_for_event(event_id),
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
        from .event_flyers import load_event_flyers

        flyer_documents = load_event_flyers()
        records = []

        for event in load_archived_schedule():
            documents = flyer_documents.get(event["id"])

            if not documents:
                continue

            first_path = documents[0]["path"]
            preview_path = (
                "flyer_previews/"
                + first_path[len("flyers/"):-4]
                + ".jpg"
            )

            records.append({
                "event": event,
                "documents": documents,
                "year": event["start_date"][:4],
                "preview": preview_path,
            })

        records.sort(
            key=lambda item: (
                item["event"]["start_date"],
                item["event"]["id"],
            ),
            reverse=True,
        )

        available_years = sorted(
            {item["year"] for item in records},
            reverse=True,
        )

        selected_year = request.args.get("year", "all")

        if selected_year not in ("all", *available_years):
            abort(400)

        query = request.args.get("q", "").strip()

        if len(query) > 120:
            abort(400)

        terms = query.casefold().split()
        filtered = []

        for item in records:
            if (
                selected_year != "all"
                and item["year"] != selected_year
            ):
                continue

            event = item["event"]

            searchable = " ".join((
                event["title"],
                event.get("location", ""),
                event["date_label"],
                event.get("category", ""),
                " ".join(
                    document["original_filename"]
                    for document in item["documents"]
                ),
            )).casefold()

            if all(term in searchable for term in terms):
                filtered.append(item)

        groups = [
            {
                "year": year,
                "items": [
                    item for item in filtered
                    if item["year"] == year
                ],
            }
            for year in available_years
        ]

        groups = [
            group for group in groups
            if group["items"]
        ]

        year_choices = [
            {
                "year": year,
                "count": sum(
                    item["year"] == year
                    for item in records
                ),
            }
            for year in available_years
        ]

        return render_template(
            "ride_flyers.html",
            flyer_groups=groups,
            flyer_years=year_choices,
            flyer_query=query,
            selected_year=selected_year,
            flyer_total_count=len(records),
            flyer_total_pdf_count=sum(
                len(item["documents"])
                for item in records
            ),
            flyer_result_count=len(filtered),
            flyer_result_pdf_count=sum(
                len(item["documents"])
                for item in filtered
            ),
        )

    @app.get("/galleries")
    def galleries():
        from .photo_albums import load_photo_albums

        return render_template(
            "galleries.html",
            photo_albums=sorted(
                load_photo_albums(),
                key=lambda album: album.get("date") or "",
                reverse=True,
            ),
        )

    @app.get("/galleries/<slug>")
    def gallery_album(slug):
        from .photo_albums import load_photo_albums

        album = next(
            (
                item for item in load_photo_albums()
                if item["slug"] == slug
            ),
            None,
        )

        if album is None:
            abort(404)

        return render_template(
            "gallery_album.html",
            album=album,
        )

    @app.get("/riding-areas")
    def riding_areas():
        from flask import request
        from .riding_area_maps import load_riding_area_maps

        records = load_riding_area_maps()
        query = request.args.get("q", "").strip()[:100]
        needle = query.casefold()

        selected = [
            item for item in records
            if not needle or needle in (
                item["title"] + " " +
                item["original_filename"]
            ).casefold()
        ]

        return render_template(
            "riding_areas.html",
            riding_maps=selected,
            map_query=query,
            map_total=len(records),
        )

    @app.get("/about")
    def about():
        return render_template(
            "section.html", page=PAGES["about"]
        )

    return app
