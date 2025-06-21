def get_with_default(key: str, data: dict, default="Unknown"):
    return data.get(key, default)


def format_player_data(data: dict) -> str:
    """Format a player data object into a readable string."""
    return f"""
        ID: {get_with_default('id', data)}
        Full Name: {get_with_default('fullName', data)}
        Link: {get_with_default('link', data)}
        First Name: {get_with_default('firstName', data)}
        Last Name: {get_with_default('lastName', data)}
        Primary Number: {get_with_default('primaryNumber', data)}
        Birth Date: {get_with_default('birthDate', data)}
        Current Age: {get_with_default('currentAge', data)}
        Birth City: {get_with_default('birthCity', data)}
        Birth Country: {get_with_default('birthCountry', data)}
        Height: {get_with_default('height', data)}
        Weight: {get_with_default('weight', data)}
        Active: {get_with_default('active', data)}
        Primary Position: {get_with_default('primaryPosition', data)}
        Use Name: {get_with_default('useName', data)}
        Use Last Name: {get_with_default('useLastName', data)}
        Boxscore Name: {get_with_default('boxscoreName', data)}
        Nick Name: {get_with_default('nickName', data)}
        Gender: {get_with_default('gender', data)}
        Is Player: {get_with_default('isPlayer', data)}
        Is Verified: {get_with_default('isVerified', data)}
        Pronunciation: {get_with_default('pronunciation', data)}
        MLB Debut Date: {get_with_default('mlbDebutDate', data)}
        Bat Side: {get_with_default('batSide', data)}
        Pitch Hand: {get_with_default('pitchHand', data)}
        Name First Last: {get_with_default('nameFirstLast', data)}
        Name Slug: {get_with_default('nameSlug', data)}
        First Last Name: {get_with_default('firstLastName', data)}
        Last First Name: {get_with_default('lastFirstName', data)}
        Last Init Name: {get_with_default('lastInitName', data)}
        Init Last Name: {get_with_default('initLastName', data)}
        Full FML Name: {get_with_default('fullFMLName', data)}
        Full LFM Name: {get_with_default('fullLFMName', data)}
        Strike Zone Top: {get_with_default('strikeZoneTop', data)}
        Strike Zone Bottom: {get_with_default('strikeZoneBottom', data)}
        """