import json
import shlex
import subprocess
import sys
from pathlib import Path

def test_semantic_profile_is_inert_and_unicode_preserving():
    profile = json.loads((Path(__file__).resolve().parents[1] / 'profiles/semantic-v1.json').read_text())
    assert profile['envelope'] == 'wellmanifest.nl-plan/v1'
    assert profile['unicode'] == 'preserve'
    assert not profile['lexical_admission'] and not profile['compilation_executes']
    assert profile['statuses'] == ['ok', 'clarify', 'unsupported']
    assert profile['runtime_owner'] == 'paxlet-com/dockuri'


def test_adopted_guard_command_runs_in_a_git_workspace(tmp_path):
    root = Path(__file__).resolve().parents[1]
    commands = [line.strip().removeprefix('command:').strip()
                for line in (root / 'worktree-guard.yaml').read_text().splitlines()
                if line.strip().startswith('command:')]
    assert len(commands) == 1
    argv = shlex.split(commands[0])
    assert argv[0] == 'python3'
    assert argv[2:] == ['--workspace-root', '{workdir}']
    subprocess.run(['git', 'init', '--quiet', '--initial-branch=main', str(tmp_path)],
                   check=True, capture_output=True)
    result = subprocess.run(
        [sys.executable, str(root / argv[1]), '--workspace-root', str(tmp_path),
         '--format', 'json'], capture_output=True, text=True, timeout=30)
    assert result.returncode == 0, result.stderr
    report = json.loads(result.stdout)
    assert report['schema'] == 'new-project.worktree-overlap-report/v1'
    assert report['status'] == 'passed'
    assert report['summary']['checkouts'] == 1
