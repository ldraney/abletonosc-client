"""Tests for Clip operations.

Uses the test_clip_with_notes fixture which creates a temporary MIDI track
with an audible clip for testing. This ensures tests are self-contained
and don't require manual setup.
"""

import pytest

from osc_client.clip import Note


def test_note_creation():
    """Test Note namedtuple creation."""
    note = Note(pitch=60, start_time=0.0, duration=0.5, velocity=100)
    assert note.pitch == 60
    assert note.start_time == 0.0
    assert note.duration == 0.5
    assert note.velocity == 100
    assert note.mute is False

    muted_note = Note(pitch=60, start_time=0.0, duration=0.5, velocity=100, mute=True)
    assert muted_note.mute is True


def test_get_name(clip, test_clip_with_notes):
    """Test getting clip name."""
    t, s = test_clip_with_notes["track"], test_clip_with_notes["scene"]
    name = clip.get_name(t, s)
    assert isinstance(name, str)


def test_set_name(clip, test_clip_with_notes):
    """Test setting clip name."""
    t, s = test_clip_with_notes["track"], test_clip_with_notes["scene"]
    original = clip.get_name(t, s)
    try:
        clip.set_name(t, s, "Test Clip")
        assert clip.get_name(t, s) == "Test Clip"
    finally:
        clip.set_name(t, s, original)


def test_get_length(clip, test_clip_with_notes):
    """Test getting clip length."""
    t, s = test_clip_with_notes["track"], test_clip_with_notes["scene"]
    length = clip.get_length(t, s)
    assert length == 4.0  # We created a 4-beat clip


def test_get_is_playing(clip, test_clip_with_notes):
    """Test checking if clip is playing."""
    t, s = test_clip_with_notes["track"], test_clip_with_notes["scene"]
    is_playing = clip.get_is_playing(t, s)
    assert isinstance(is_playing, bool)


def test_get_color(clip, test_clip_with_notes):
    """Test getting clip color."""
    t, s = test_clip_with_notes["track"], test_clip_with_notes["scene"]
    color = clip.get_color(t, s)
    assert isinstance(color, int)


def test_get_loop_start(clip, test_clip_with_notes):
    """Test getting loop start."""
    t, s = test_clip_with_notes["track"], test_clip_with_notes["scene"]
    loop_start = clip.get_loop_start(t, s)
    assert isinstance(loop_start, float)
    assert loop_start >= 0


def test_get_loop_end(clip, test_clip_with_notes):
    """Test getting loop end."""
    t, s = test_clip_with_notes["track"], test_clip_with_notes["scene"]
    loop_end = clip.get_loop_end(t, s)
    assert isinstance(loop_end, float)
    assert loop_end > 0


def test_get_notes(clip, test_clip_with_notes):
    """Test getting notes from a clip."""
    t, s = test_clip_with_notes["track"], test_clip_with_notes["scene"]
    notes = clip.get_notes(t, s)
    assert len(notes) == 3  # C major chord (C, E, G)
    pitches = [n.pitch for n in notes]
    assert 60 in pitches  # C4
    assert 64 in pitches  # E4
    assert 67 in pitches  # G4


def test_is_midi_clip(clip, test_clip_with_notes):
    """Test checking if clip is a MIDI clip."""
    t, s = test_clip_with_notes["track"], test_clip_with_notes["scene"]
    assert clip.get_is_midi_clip(t, s) is True
    assert clip.get_is_audio_clip(t, s) is False


# Phase 8: Clip properties tests


def test_get_start_time(clip, test_clip_with_notes):
    """Test getting clip start time."""
    t, s = test_clip_with_notes["track"], test_clip_with_notes["scene"]
    start_time = clip.get_start_time(t, s)
    assert isinstance(start_time, float)


def test_get_end_time(clip, test_clip_with_notes):
    """Test getting clip end time."""
    t, s = test_clip_with_notes["track"], test_clip_with_notes["scene"]
    end_time = clip.get_end_time(t, s)
    assert isinstance(end_time, float)
    assert end_time > 0


def test_get_looping(clip, test_clip_with_notes):
    """Test getting clip looping state."""
    t, s = test_clip_with_notes["track"], test_clip_with_notes["scene"]
    looping = clip.get_looping(t, s)
    assert isinstance(looping, bool)


def test_set_looping(clip, test_clip_with_notes):
    """Test setting clip looping state."""
    t, s = test_clip_with_notes["track"], test_clip_with_notes["scene"]
    original = clip.get_looping(t, s)
    try:
        clip.set_looping(t, s, True)
        assert clip.get_looping(t, s) is True

        clip.set_looping(t, s, False)
        assert clip.get_looping(t, s) is False
    finally:
        clip.set_looping(t, s, original)


def test_duplicate_loop(clip, test_clip_with_notes):
    """Test duplicating loop (just verify no error)."""
    t, s = test_clip_with_notes["track"], test_clip_with_notes["scene"]
    # Just verify method executes without error
    clip.duplicate_loop(t, s)


def test_get_pitch_coarse(clip, test_clip_with_notes):
    """Test getting coarse pitch adjustment (returns 0 for MIDI clips)."""
    t, s = test_clip_with_notes["track"], test_clip_with_notes["scene"]
    pitch = clip.get_pitch_coarse(t, s)
    assert isinstance(pitch, int)
    # MIDI clips return 0, audio clips return -48 to +48
    assert -48 <= pitch <= 48


def test_get_pitch_fine(clip, test_clip_with_notes):
    """Test getting fine pitch adjustment (returns 0 for MIDI clips)."""
    t, s = test_clip_with_notes["track"], test_clip_with_notes["scene"]
    pitch = clip.get_pitch_fine(t, s)
    assert isinstance(pitch, float)
    # MIDI clips return 0, audio clips return -50 to +50
    assert -50 <= pitch <= 50
