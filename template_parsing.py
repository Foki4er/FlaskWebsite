import pymorphy2

def teplate_parsing(institution_director_short, classe):
    morph = pymorphy2.MorphAnalyzer()

    names = institution_director_short[1]
    name_lower = names.lower()
    parsed_word = morph.parse(name_lower)[0]
    declination_gender = parsed_word.tag.gender

    if declination_gender == "masc":
        dative_surname = institution_director_short[0] + 'у'
        respect = "Уважаемый"
    elif declination_gender == "femn":
        dative_surname = (institution_director_short[0])[:-1] + 'ой'
        respect = "Уважаемая"
    return (dative_surname, respect)