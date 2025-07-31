import instaloader

def search_instagram_bios(keyword, max_profiles=10):
    L = instaloader.Instaloader()
    results = []
    # טעינת פרופילים לדוגמה (רשימה מקומית או דרך חיפוש hashtag)
    for profile_name in ["example1", "example2"]:  # placeholder
        profile = instaloader.Profile.from_username(L.context, profile_name)
        if keyword.lower() in profile.biography.lower():
            results.append({
                "title": profile.username,
                "url": f"https://instagram.com/{profile.username}",
                "bio": profile.biography
            })
        if len(results) >= max_profiles:
            break
    return results
