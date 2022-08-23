from flask import Flask, render_template, request
from email_validator import validate_email
import os
import csv

app = Flask(__name__)

APP_FOLDER = os.path.dirname(__file__)
MAKES_MODELS = dict()
with open(os.path.join(APP_FOLDER, "static", "makes_models.csv")) as csv_file:
    rdr = csv.reader(csv_file)
    for row in rdr:
        make = row[0]
        model = row[1]
        if make not in MAKES_MODELS:
            MAKES_MODELS[make] = []
        MAKES_MODELS[make].append(model)


@app.route("/")
@app.route("/index")
def index():
    menu = {
        "introduction": [
            ["Me", "about_me"],
            ["htmx", "about_htmx"],
            ["hyperscript", "about_hyperscript"],
            ["This Site", "about_this_site"]
        ],
        "htmx demos": [
            ["Inline Validation", "inline_validation"],
            ["Dependent Dropdown", "dependent_dropdown"],
            ["Active Search", "active_search"],
        ],
        "hyperscript": [["hyperscript Examples", "hyperscript_examples"]],
        "exercises": [
            ["Inline Validation", "ex_inline_validation"],
            ["Dependent Dropdown", "ex_dependent_dropdown"],
            ["Active Search", "ex_active_search"],
            ["hyperscript Examples", "ex_hyperscript_examples"],
        ],
        "reference": [
            ["Articles/Videos", "articles_videos"],
            ["htmx.org", "https://htmx.org", "off"],
            ["hyperscript.org", "https://hyperscript.org", "off"],
        ],
    }
    return render_template("index.html", menu=menu)


@app.route("/about_me")
def about_me():
    return render_template("about_me.html")


@app.route("/about_htmx")
def about_htmx():
    return render_template("about_htmx.html")


@app.route("/about_hyperscript")
def about_hyperscript():
    return render_template("about_hyperscript.html")


@app.route("/about_this_site")
def about_this_site():
    return render_template("about_this_site.html"

                           )
@app.route("/articles_videos")
def articles_videos():
    return render_template("articles_videos.html")


@app.route("/inline_validation")
def inline_validation():
    return render_template("inline_validation.html")


@app.route("/validate_email", methods=["POST"])
def validate_email_address():
    email_address = request.form.get("email")
    try:
        email = validate_email(email_address).email
        return ""
    except:
        return "Invalid Email Address"


@app.route("/dependent_dropdown")
def dependent_dropdown():
    return render_template("dependent_dropdown.html", makes_models=sorted(MAKES_MODELS))


@app.route("/get_models")
def get_models():
    models = MAKES_MODELS[request.args.get("make")]

    return render_template("models.html", models=sorted(models))


@app.route("/active_search")
def active_search():
    return render_template("active_search.html")


@app.route("/get_search_results", methods=["POST"])
def get_search_results():
    search_text = request.form.get("search_text")
    search_results = []

    if search_text:
        for make in MAKES_MODELS:
            for model in MAKES_MODELS[make]:
                if search_text.lower() in model.lower():
                    search_results.append(f"{model} [{make}]")

        if len(search_results) == 0:
            search_results.append("No matches found")

    return render_template("search_results.html", search_results=sorted(search_results))


@app.route("/hyperscript_examples")
def hyperscript_examples():
    return render_template("hyperscript_examples.html", makes=sorted(MAKES_MODELS))


@app.route("/ex_inline_validation")
def ex_inline_validation():
    return render_template("exercises/inline_validation.html")


@app.route("/ex_dependent_dropdown")
def ex_dependent_dropdown():
    return render_template(
        "exercises/dependent_dropdown.html", makes_models=sorted(MAKES_MODELS)
    )


@app.route("/ex_active_search")
def ex_active_search():
    return render_template("exercises/active_search.html")


@app.route("/ex_hyperscript_examples")
def ex_hyperscript_examples():
    return render_template(
        "exercises/hyperscript_examples.html", makes=sorted(MAKES_MODELS)
    )


if __name__ == '__main__':
    app.run(debug=True)
