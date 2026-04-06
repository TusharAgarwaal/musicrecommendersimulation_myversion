import csv
from typing import List, Dict, Tuple
from dataclasses import dataclass

MAX_BPM = 160.0


@dataclass
class Song:
    """
    Represents a song and its attributes.
    Required by tests/test_recommender.py
    """
    id: int
    title: str
    artist: str
    genre: str
    mood: str
    energy: float
    tempo_bpm: float
    valence: float
    danceability: float
    acousticness: float


@dataclass
class UserProfile:
    """
    Represents a user's taste preferences.
    Required by tests/test_recommender.py
    """
    favorite_genre: str
    favorite_mood: str
    target_energy: float
    target_bpm: float
    likes_acoustic: bool


# Added: Algorithm Recipe scoring — returns (score out of 10, list of reasons)
def score_song(song: Song, user: UserProfile) -> Tuple[float, List[str]]:
    """
    Scores a song against a user profile using the Algorithm Recipe.
    Returns (score out of 10, list of reason strings).
    """
    reasons = []
    total = 0.0

    # Genre — categorical, max 3.0
    if song.genre == user.favorite_genre:
        total += 3.0
        reasons.append(f"genre match (+3.0)")

    # Mood — categorical, max 2.0
    if song.mood == user.favorite_mood:
        total += 2.0
        reasons.append(f"mood match (+2.0)")

    # Intensity — numerical (Algorithm Recipe), max 3.0
    user_intensity = 0.5 * user.target_energy + 0.5 * (user.target_bpm / MAX_BPM)
    song_intensity = 0.5 * song.energy + 0.5 * (song.tempo_bpm / MAX_BPM)
    intensity_pts = round(3.0 * (1.0 - abs(user_intensity - song_intensity)), 2)
    total += intensity_pts
    reasons.append(f"intensity ({song_intensity:.2f}) match (+{intensity_pts})")

    # Acousticness — numerical, max 1.0
    acoustic_pts = round(song.acousticness if user.likes_acoustic else 1.0 - song.acousticness, 2)
    total += acoustic_pts
    reasons.append(f"acousticness match (+{acoustic_pts})")

    # Valence — numerical, max 1.0
    valence_pts = round(1.0 * (1.0 - abs(0.7 - song.valence)), 2)
    total += valence_pts
    reasons.append(f"valence match (+{valence_pts})")

    return round(total, 2), reasons


class Recommender:
    """
    OOP implementation of the recommendation logic.
    Required by tests/test_recommender.py
    """
    def __init__(self, songs: List[Song]):
        self.songs = songs

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        scored = sorted(self.songs, key=lambda s: score_song(s, user)[0], reverse=True)
        return scored[:k]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        _, reasons = score_song(song, user)
        return ", ".join(reasons)


# Added: CSV loader — reads data/songs.csv and returns a list of song dicts
def load_songs(csv_path: str) -> List[Dict]:
    """
    Loads songs from a CSV file.
    Required by src/main.py
    """
    songs = []
    with open(csv_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            songs.append({
                "id":           int(row["id"]),
                "title":        row["title"],
                "artist":       row["artist"],
                "genre":        row["genre"],
                "mood":         row["mood"],
                "energy":       float(row["energy"]),
                "tempo_bpm":    float(row["tempo_bpm"]),
                "valence":      float(row["valence"]),
                "danceability": float(row["danceability"]),
                "acousticness": float(row["acousticness"]),
            })
    return songs


# Added: dict-based version of Algorithm Recipe scoring used by recommend_songs
def _score_song_dict(song: Dict, user_prefs: Dict) -> Tuple[float, List[str]]:
    reasons = []
    total = 0.0

    if song["genre"] == user_prefs["genre"]:
        total += 3.0
        reasons.append("genre match (+3.0)")

    if song["mood"] == user_prefs["mood"]:
        total += 2.0
        reasons.append("mood match (+2.0)")

    user_intensity = 0.5 * user_prefs["energy"] + 0.5 * (user_prefs["target_bpm"] / MAX_BPM)
    song_intensity = 0.5 * song["energy"] + 0.5 * (song["tempo_bpm"] / MAX_BPM)
    intensity_pts = round(3.0 * (1.0 - abs(user_intensity - song_intensity)), 2)
    total += intensity_pts
    reasons.append(f"intensity ({song_intensity:.2f}) match (+{intensity_pts})")

    likes_acoustic = user_prefs.get("likes_acoustic", False)
    acoustic_pts = round(song["acousticness"] if likes_acoustic else 1.0 - song["acousticness"], 2)
    total += acoustic_pts
    reasons.append(f"acousticness match (+{acoustic_pts})")

    valence_pts = round(1.0 * (1.0 - abs(0.7 - song["valence"])), 2)
    total += valence_pts
    reasons.append(f"valence match (+{valence_pts})")

    return round(total, 2), reasons


# Added: functional entry point — judges every song, sorts by score, returns top k with explanations
def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    """
    Functional implementation of the recommendation logic.
    Required by src/main.py
    """
    scored = []
    for song in songs:
        song_score, reasons = _score_song_dict(song, user_prefs)
        explanation = ", ".join(reasons)
        scored.append((song, song_score, explanation))

    scored.sort(key=lambda x: x[1], reverse=True)
    return scored[:k]
