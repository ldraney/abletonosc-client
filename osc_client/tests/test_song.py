"""Tests for Song operations."""

import time

SETTLE_TIME = 0.1  # Time for Ableton to process changes


def test_get_tempo(song):
    """Test getting current tempo."""
    tempo = song.get_tempo()
    assert 20 <= tempo <= 999  # Valid BPM range


def test_set_tempo(song):
    """Test setting tempo."""
    original = song.get_tempo()
    try:
        song.set_tempo(120.0)
        assert song.get_tempo() == 120.0

        song.set_tempo(140.5)
        assert song.get_tempo() == 140.5
    finally:
        song.set_tempo(original)  # Restore


def test_get_is_playing(song):
    """Test getting play state."""
    is_playing = song.get_is_playing()
    assert isinstance(is_playing, bool)


def test_start_stop_playing(song):
    """Test transport controls."""
    original_playing = song.get_is_playing()
    try:
        song.stop_playing()
        time.sleep(SETTLE_TIME)
        assert song.get_is_playing() is False

        song.start_playing()
        time.sleep(SETTLE_TIME)
        assert song.get_is_playing() is True

        song.stop_playing()
        time.sleep(SETTLE_TIME)
        assert song.get_is_playing() is False
    finally:
        if original_playing:
            song.start_playing()
        else:
            song.stop_playing()


def test_get_num_tracks(song):
    """Test getting track count."""
    num_tracks = song.get_num_tracks()
    assert num_tracks >= 1  # Always at least one track


def test_get_num_scenes(song):
    """Test getting scene count."""
    num_scenes = song.get_num_scenes()
    assert num_scenes >= 1  # Always at least one scene


def test_get_signature(song):
    """Test getting time signature."""
    numerator = song.get_signature_numerator()
    denominator = song.get_signature_denominator()

    assert 1 <= numerator <= 99
    assert denominator in [1, 2, 4, 8, 16]  # Powers of 2


def test_set_signature(song):
    """Test setting time signature."""
    original_num = song.get_signature_numerator()
    original_denom = song.get_signature_denominator()
    try:
        song.set_signature_numerator(3)
        song.set_signature_denominator(4)

        assert song.get_signature_numerator() == 3
        assert song.get_signature_denominator() == 4
    finally:
        song.set_signature_numerator(original_num)
        song.set_signature_denominator(original_denom)


def test_get_metronome(song):
    """Test getting metronome state."""
    metronome = song.get_metronome()
    assert isinstance(metronome, bool)


def test_set_metronome(song):
    """Test toggling metronome."""
    original = song.get_metronome()
    try:
        song.set_metronome(True)
        assert song.get_metronome() is True

        song.set_metronome(False)
        assert song.get_metronome() is False
    finally:
        song.set_metronome(original)


def test_get_current_song_time(song):
    """Test getting playback position."""
    position = song.get_current_song_time()
    assert isinstance(position, float)
    assert position >= 0


def test_create_and_delete_midi_track(song):
    """Test creating and deleting a MIDI track."""
    original_count = song.get_num_tracks()

    # Create MIDI track at end
    song.create_midi_track(-1)
    time.sleep(SETTLE_TIME)
    assert song.get_num_tracks() == original_count + 1

    # Delete the new track
    song.delete_track(original_count)
    time.sleep(SETTLE_TIME)
    assert song.get_num_tracks() == original_count


def test_create_and_delete_audio_track(song):
    """Test creating and deleting an audio track."""
    original_count = song.get_num_tracks()

    # Create audio track at end
    song.create_audio_track(-1)
    time.sleep(SETTLE_TIME)
    assert song.get_num_tracks() == original_count + 1

    # Delete the new track
    song.delete_track(original_count)
    time.sleep(SETTLE_TIME)
    assert song.get_num_tracks() == original_count


def test_duplicate_track(song):
    """Test duplicating a track."""
    original_count = song.get_num_tracks()

    # Duplicate track 0
    song.duplicate_track(0)
    time.sleep(SETTLE_TIME)
    assert song.get_num_tracks() == original_count + 1

    # Delete the duplicate (it appears at index 1)
    song.delete_track(1)
    time.sleep(SETTLE_TIME)
    assert song.get_num_tracks() == original_count


def test_get_groove_amount(song):
    """Test getting groove amount."""
    groove = song.get_groove_amount()
    assert 0.0 <= groove <= 1.0


def test_set_groove_amount(song):
    """Test setting groove amount."""
    original = song.get_groove_amount()
    try:
        song.set_groove_amount(0.5)
        time.sleep(SETTLE_TIME)
        assert abs(song.get_groove_amount() - 0.5) < 0.01

        song.set_groove_amount(0.0)
        time.sleep(SETTLE_TIME)
        assert abs(song.get_groove_amount()) < 0.01
    finally:
        song.set_groove_amount(original)


def test_can_undo_redo(song):
    """Test undo/redo availability checks."""
    can_undo = song.can_undo()
    can_redo = song.can_redo()

    # These return bools regardless of state
    assert isinstance(can_undo, bool)
    assert isinstance(can_redo, bool)


def test_undo_redo(song):
    """Test undo and redo functionality."""
    # Make a change we can undo
    original_tempo = song.get_tempo()
    new_tempo = 130.0 if original_tempo != 130.0 else 125.0

    song.set_tempo(new_tempo)
    time.sleep(SETTLE_TIME)
    assert song.get_tempo() == new_tempo

    # Undo should revert
    if song.can_undo():
        song.undo()
        time.sleep(SETTLE_TIME)
        # Tempo should be back to original
        assert song.get_tempo() == original_tempo

        # Redo should reapply
        if song.can_redo():
            song.redo()
            time.sleep(SETTLE_TIME)
            assert song.get_tempo() == new_tempo

            # Clean up - undo back to original
            song.undo()
            time.sleep(SETTLE_TIME)


def test_stop_all_clips(song):
    """Test stopping all clips."""
    # Just verify the method executes without error
    # We can't easily verify clips stopped without playing one first
    song.stop_all_clips()


def test_capture_midi(song):
    """Test MIDI capture (just verify no error)."""
    # capture_midi requires recently played MIDI, so we just
    # verify it doesn't raise an exception
    song.capture_midi()
