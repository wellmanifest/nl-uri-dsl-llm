import json
from pathlib import Path

def test_semantic_profile_is_inert_and_unicode_preserving():
    profile = json.loads((Path(__file__).resolve().parents[1] / 'profiles/semantic-v1.json').read_text())
    assert profile['envelope'] == 'wellmanifest.nl-plan/v1'
    assert profile['unicode'] == 'preserve'
    assert not profile['lexical_admission'] and not profile['compilation_executes']
    assert profile['statuses'] == ['ok', 'clarify', 'unsupported']
    assert profile['runtime_owner'] == 'paxlet-com/dockuri'
