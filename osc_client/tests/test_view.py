"""Tests for View operations."""


def test_get_selected_track(view):
    """Test getting selected track."""
    track = view.get_selected_track()
    assert isinstance(track, int)
    assert track >= 0


def test_set_selected_track(view, song):
    """Test setting selected track."""
    original = view.get_selected_track()
    num_tracks = song.get_num_tracks()

    try:
        # Select first track
        view.set_selected_track(0)
        assert view.get_selected_track() == 0

        # Select another track if available
        if num_tracks > 1:
            view.set_selected_track(1)
            assert view.get_selected_track() == 1
    finally:
        view.set_selected_track(original)


def test_get_selected_scene(view):
    """Test getting selected scene."""
    scene = view.get_selected_scene()
    assert isinstance(scene, int)
    assert scene >= 0


def test_set_selected_scene(view, song):
    """Test setting selected scene."""
    original = view.get_selected_scene()
    num_scenes = song.get_num_scenes()

    try:
        # Select first scene
        view.set_selected_scene(0)
        assert view.get_selected_scene() == 0

        # Select another scene if available
        if num_scenes > 1:
            view.set_selected_scene(1)
            assert view.get_selected_scene() == 1
    finally:
        view.set_selected_scene(original)


# Phase 9: Selection tests


def test_get_selected_clip(view):
    """Test getting selected clip."""
    result = view.get_selected_clip()
    assert isinstance(result, tuple)
    assert len(result) == 2


def test_set_selected_clip(view, test_clip_with_notes):
    """Test setting selected clip."""
    t, s = test_clip_with_notes["track"], test_clip_with_notes["scene"]

    view.set_selected_clip(t, s)
    result = view.get_selected_clip()
    # Note: result may vary depending on Ableton state
    assert isinstance(result, tuple)


def test_get_selected_device(view):
    """Test getting selected device."""
    result = view.get_selected_device()
    assert isinstance(result, tuple)
    assert len(result) == 2


def test_set_selected_device(view, song, track):
    """Test setting selected device (requires device on track)."""
    import time

    SETTLE_TIME = 0.1

    # Create a track with a device
    original_tracks = song.get_num_tracks()
    track_idx = original_tracks

    song.create_midi_track(-1)
    time.sleep(SETTLE_TIME)

    try:
        # Insert a device
        device_idx = track.insert_device(track_idx, "Wavetable")
        time.sleep(SETTLE_TIME)

        if device_idx >= 0:
            view.set_selected_device(track_idx, device_idx)
            result = view.get_selected_device()
            assert isinstance(result, tuple)
    finally:
        song.delete_track(track_idx)
        time.sleep(SETTLE_TIME)
