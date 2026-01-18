"""
Lofi Midnight Rain
A late-night lofi track with melancholic vibes.

Key: F minor | Tempo: 70 BPM | Length: 8 bars
"""

import time
import sys
sys.path.insert(0, '/Users/ldraney/ableton-music-development')

from osc_client import connect
from osc_client.song import Song
from osc_client.track import Track
from osc_client.clip_slot import ClipSlot
from osc_client.clip import Clip, Note


def create_song():
    client = connect()
    song = Song(client)
    track_api = Track(client)
    clip_slot = ClipSlot(client)
    clip = Clip(client)

    print("=== Lofi Midnight Rain ===\n")

    # Set tempo - slower for late night vibes
    song.set_tempo(70.0)
    print("✓ Tempo: 70 BPM")

    start_tracks = song.get_num_tracks()

    # ============================================================
    # TRACK 1: DRUMS - slow, laid back
    # ============================================================
    print("\n--- Drums ---")
    drum_idx = start_tracks
    song.create_midi_track(-1)
    time.sleep(0.3)
    track_api.set_name(drum_idx, "MR Drums")
    track_api.insert_device(drum_idx, "Drum Rack")
    time.sleep(0.3)

    clip_slot.create_clip(drum_idx, 0, 32.0)  # 8 bars
    time.sleep(0.2)

    KICK = 36
    SNARE = 38
    HIHAT = 42
    SHAKER = 70

    drum_notes = []
    for bar in range(8):
        offset = bar * 4.0

        # Sparse kick - just on 1 and occasionally on 3
        drum_notes.append(Note(KICK, offset + 0.0, 0.5, 90))
        if bar % 2 == 0:
            drum_notes.append(Note(KICK, offset + 2.5, 0.25, 65))

        # Snare on 2 and 4, softer
        drum_notes.append(Note(SNARE, offset + 1.0, 0.5, 75))
        drum_notes.append(Note(SNARE, offset + 3.0, 0.5, 80))

        # Gentle hi-hats, very swung
        for i in range(8):
            hat_time = offset + (i * 0.5)
            if i % 2 == 1:
                hat_time += 0.1  # heavy swing
            vel = 55 if i % 2 == 0 else 35
            drum_notes.append(Note(HIHAT, hat_time, 0.15, vel))

    clip.add_notes(drum_idx, 0, drum_notes)
    print(f"  {len(drum_notes)} hits")

    # ============================================================
    # TRACK 2: BASS - deep and simple
    # ============================================================
    print("\n--- Bass ---")
    bass_idx = start_tracks + 1
    song.create_midi_track(-1)
    time.sleep(0.3)
    track_api.set_name(bass_idx, "MR Bass")
    track_api.insert_device(bass_idx, "Operator")
    time.sleep(0.3)

    clip_slot.create_clip(bass_idx, 0, 32.0)
    time.sleep(0.2)

    # F minor progression: Fm - Db - Ab - Eb (2 bars each)
    # F2=41, Db2=37, Ab2=44, Eb2=39
    bass_notes = []
    bass_pattern = [
        # Bars 1-2: Fm (F2 = 41)
        (0.0, 41, 3.0), (3.5, 41, 0.5),
        (4.0, 41, 2.0), (6.5, 43, 0.5), (7.0, 41, 1.0),
        # Bars 3-4: Db (Db2 = 37)
        (8.0, 37, 3.0), (11.5, 37, 0.5),
        (12.0, 37, 2.0), (14.5, 39, 0.5), (15.0, 37, 1.0),
        # Bars 5-6: Ab (Ab2 = 44)
        (16.0, 44, 3.0), (19.5, 44, 0.5),
        (20.0, 44, 2.0), (22.5, 46, 0.5), (23.0, 44, 1.0),
        # Bars 7-8: Eb (Eb2 = 39)
        (24.0, 39, 3.0), (27.5, 39, 0.5),
        (28.0, 39, 2.0), (30.5, 41, 0.5), (31.0, 39, 1.0),
    ]

    for start, pitch, dur in bass_pattern:
        bass_notes.append(Note(pitch, start, dur, 80))

    clip.add_notes(bass_idx, 0, bass_notes)
    print(f"  {len(bass_notes)} notes")

    # ============================================================
    # TRACK 3: KEYS - Rhodes-style 7th chords
    # ============================================================
    print("\n--- Keys ---")
    keys_idx = start_tracks + 2
    song.create_midi_track(-1)
    time.sleep(0.3)
    track_api.set_name(keys_idx, "MR Keys")
    result = track_api.insert_device(keys_idx, "Electric")
    if result < 0:
        track_api.insert_device(keys_idx, "Wavetable")
    time.sleep(0.3)

    clip_slot.create_clip(keys_idx, 0, 32.0)
    time.sleep(0.2)

    # Jazz voicings in F minor
    # Fm7: F Ab C Eb -> voiced: F3 C4 Eb4 Ab4
    fm7 = [53, 60, 63, 68]
    # Dbmaj7: Db F Ab C -> voiced: Db3 Ab3 C4 F4
    dbmaj7 = [49, 56, 60, 65]
    # Abmaj7: Ab C Eb G -> voiced: Ab3 Eb4 G4 C5
    abmaj7 = [56, 63, 67, 72]
    # Eb7: Eb G Bb Db -> voiced: Eb3 Bb3 Db4 G4
    eb7 = [51, 58, 61, 67]

    keys_notes = []
    chord_seq = [
        (0.0, fm7, 7.5),
        (8.0, dbmaj7, 7.5),
        (16.0, abmaj7, 7.5),
        (24.0, eb7, 7.5),
    ]

    for start, chord, dur in chord_seq:
        for i, pitch in enumerate(chord):
            strum = i * 0.04
            vel = 65 - (i * 4)
            keys_notes.append(Note(pitch, start + strum, dur, vel))

    clip.add_notes(keys_idx, 0, keys_notes)
    print(f"  {len(keys_notes)} notes")

    # ============================================================
    # TRACK 4: PAD - warm wash
    # ============================================================
    print("\n--- Pad ---")
    pad_idx = start_tracks + 3
    song.create_midi_track(-1)
    time.sleep(0.3)
    track_api.set_name(pad_idx, "MR Pad")
    track_api.insert_device(pad_idx, "Wavetable")
    time.sleep(0.3)
    track_api.set_volume(pad_idx, 0.45)

    clip_slot.create_clip(pad_idx, 0, 32.0)
    time.sleep(0.2)

    pad_notes = []
    # Higher, airier voicings
    pad_chords = [
        (0.0, [65, 68, 72, 75], 8.0),   # Fm (F4 Ab4 C5 Eb5)
        (8.0, [61, 65, 68, 72], 8.0),   # Db (Db4 F4 Ab4 C5)
        (16.0, [68, 72, 75, 79], 8.0),  # Ab (Ab4 C5 Eb5 G5)
        (24.0, [63, 67, 70, 75], 8.0),  # Eb (Eb4 G4 Bb4 Eb5)
    ]

    for start, pitches, dur in pad_chords:
        for p in pitches:
            pad_notes.append(Note(p, start, dur, 40))

    clip.add_notes(pad_idx, 0, pad_notes)
    print(f"  {len(pad_notes)} notes")

    # ============================================================
    # TRACK 5: MELODY - F minor pentatonic
    # ============================================================
    print("\n--- Melody ---")
    mel_idx = start_tracks + 4
    song.create_midi_track(-1)
    time.sleep(0.3)
    track_api.set_name(mel_idx, "MR Melody")
    track_api.insert_device(mel_idx, "Wavetable")
    time.sleep(0.3)
    track_api.set_volume(mel_idx, 0.65)

    clip_slot.create_clip(mel_idx, 0, 32.0)
    time.sleep(0.2)

    # F minor pentatonic: F Ab Bb C Eb
    # Simple, sparse, melancholic melody
    melody = [
        # Over Fm7
        (1.0, 77, 1.5, 70),    # F5
        (3.0, 75, 0.75, 65),   # Eb5
        (4.0, 72, 2.0, 75),    # C5
        (6.5, 70, 0.5, 60),    # Bb4
        (7.0, 68, 1.0, 70),    # Ab4

        # Over Dbmaj7
        (9.0, 72, 1.0, 70),    # C5
        (10.5, 68, 0.75, 65),  # Ab4
        (11.5, 65, 2.5, 75),   # F4

        # Over Abmaj7
        (16.5, 68, 1.0, 70),   # Ab4
        (18.0, 72, 1.5, 75),   # C5
        (20.0, 75, 1.0, 70),   # Eb5
        (21.5, 77, 2.0, 80),   # F5 (peak)

        # Over Eb7 - descend and resolve
        (24.5, 75, 0.75, 70),  # Eb5
        (25.5, 72, 0.75, 65),  # C5
        (26.5, 70, 0.75, 65),  # Bb4
        (27.5, 68, 1.0, 70),   # Ab4
        (29.0, 65, 3.0, 75),   # F4 (resolve)
    ]

    mel_notes = []
    for start, pitch, dur, vel in melody:
        mel_notes.append(Note(pitch, start, dur, vel))

    clip.add_notes(mel_idx, 0, mel_notes)
    print(f"  {len(mel_notes)} notes")

    # ============================================================
    # FIRE ALL CLIPS
    # ============================================================
    print("\n=== Playing ===")
    time.sleep(0.3)

    for i in range(5):
        clip_slot.fire(start_tracks + i, 0)
        time.sleep(0.05)

    print("\n🌧️  LOFI MIDNIGHT RAIN  🌧️")
    print("   Key: F minor")
    print("   Tempo: 70 BPM")
    print("   Progression: Fm7 - Dbmaj7 - Abmaj7 - Eb7")
    print("\n   Late night vibes...")

    client.close()


if __name__ == "__main__":
    create_song()
