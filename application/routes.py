from application import app, db
from flask import request, jsonify, render_template, redirect
from application.models import Pokemon
from application.forms import AddPokemonForm


def format_pokemon(pokemon):
    return {
        "id": pokemon.id,
        "name": pokemon.name,
        "ability": pokemon.ability,
        "type": pokemon.type,
    }


@app.route("/")
def index():
    return "Index Page"


@app.route("/pokemons/", methods=["GET", "POST"])
def get_pokemons():
    form = AddPokemonForm()
    if request.method == "GET":
        pokemons = Pokemon.query.all()
        pokemon_list = []
        for pokemon in pokemons:
            pokemon_list.append(format_pokemon(pokemon))
        return render_template(
            "pokemons.html",
            pokemons=pokemon_list,
            title="Pokemon",
            form=form,
        )
    else:
        if form.validate_on_submit():
            pokemon = Pokemon(form.name.data, form.ability.data, form.type.data)
            db.session.add(pokemon)
            db.session.commit()
            return redirect("/")
        # data = request.json
        # pokemon = Pokemon(data["name"], data["ability"], data["type"])
        # db.session.add(pokemon)
        # db.session.commit()
        # return jsonify(
        #     id=pokemon.id,
        #     name=pokemon.name,
        #     ability=pokemon.ability,
        #     type=pokemon.type,
        # )


@app.route("/pokemons/<id>", methods=["GET"])
def get_pokemon(id):
    pokemon = Pokemon.query.filter_by(id=id).first()
    return render_template("pokemon.html", pokemon=pokemon)


@app.route("/pokemons/<id>", methods=["DELETE"])
def delete_pokemon(id):
    pokemon = Pokemon.query.filter_by(id=id).first()
    db.session.delete(pokemon)
    db.session.commit()
    return f"{pokemon.name} deleted"


@app.route("/pokemons/<id>", methods=["PATCH"])
def update_pokemon(id):
    pokemon = Pokemon.query.filter_by(id=id)
    data = request.json
    pokemon.update(
        dict(name=data["name"], age=data["age"], catch_phrase=data["catch_phrase"])
    )
    db.session.commit()
    updated_pokemon = pokemon.first()
    return jsonify(
        id=updated_pokemon.id,
        name=updated_pokemon.name,
        age=updated_pokemon.age,
        catch_phrase=updated_pokemon.catch_phrase,
    )
