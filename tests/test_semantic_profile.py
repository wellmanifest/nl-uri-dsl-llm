import json
import shlex
import subprocess
import sys
from copy import deepcopy
from pathlib import Path

import pytest
from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[1]


@pytest.fixture
def exchange_validator():
    profile = json.loads((ROOT / 'profiles/semantic-v1.json').read_text())
    assert profile['exchange']['authority_from_envelope'] is False
    schema = profile['exchange']['schema']
    Draft202012Validator.check_schema(schema)
    return Draft202012Validator(schema)


def resource(number):
    return {
        'urn': f'urn:uuid:00000000-0000-4000-8000-{number:012d}',
        'sha256': 'a' * 64,
        'mediaType': 'application/json',
    }


def exchange(kind='request', mutation=False):
    request = resource(1)['urn']
    value = {
        'schema': 'wellmanifest.process-exchange/v1', 'kind': kind,
        'messageUrn': request if kind == 'request' else resource(2)['urn'],
        'requestUrn': request,
        'operation': 'willman://operation/koru.inspect_tasks/v1',
        'contractDigest': 'b' * 64, 'effects': ['read'],
        'inputs': [resource(3)],
    }
    if mutation:
        value.update({
            'operation': 'willman://operation/koru.develop_ticket/v1',
            'effects': ['write', 'execute'],
            'context': {
                'repositoryRef': 'semcod/koru', 'ticketId': 'ticket-427',
                'branchRef': 'ticket/427-admission-client',
                'worktreeId': 'ticket-427--admission-client',
                'ownerSession': 'fixture-session', 'planHash': 'c' * 64,
                'scopeHash': 'd' * 64, 'baseSha': 'e' * 40,
            },
        })
    if kind == 'request':
        value['arguments'] = {'prompt': 'Sprawdź kolejkę — χωρίς αλλαγές'}
    else:
        value.update(outcome='completed', outputs=[resource(4)])
        if mutation:
            value.update({
                'admission': {'request': resource(5), 'receipt': resource(6),
                              'leaseId': 'fixture-lease', 'leaseRevision': 1,
                              'fencingToken': 1},
                'verification': resource(7), 'completion': resource(8),
            })
    return value


@pytest.mark.parametrize('kind,mutation', [
    ('request', False), ('request', True), ('result', False), ('result', True),
])
def test_exchange_shape_roundtrip(exchange_validator, kind, mutation):
    value = exchange(kind, mutation)
    encoded = json.dumps(value, ensure_ascii=False)
    exchange_validator.validate(json.loads(encoded))
    if kind == 'request':
        assert 'χωρίς' in encoded and 'Sprawdź' in encoded
        assert 'admission' not in value


@pytest.mark.parametrize('outcome', ['blocked', 'failed', 'clarify', 'unsupported'])
def test_noncompleted_result_does_not_require_write_grant(exchange_validator, outcome):
    value = exchange('result', True)
    for key in ['admission', 'verification', 'completion']:
        del value[key]
    value.update(outcome=outcome, outputs=[], reason='Protected admission unavailable')
    exchange_validator.validate(value)


@pytest.mark.parametrize('field', [
    'messageUrn', 'requestUrn', 'operation', 'contractDigest', 'effects', 'inputs',
])
def test_exchange_missing_binding_rejected(exchange_validator, field):
    value = exchange()
    del value[field]
    assert list(exchange_validator.iter_errors(value))


@pytest.mark.parametrize('field', ['context', 'admission', 'verification', 'completion'])
def test_mutation_completion_requires_evidence(exchange_validator, field):
    value = exchange('result', True)
    del value[field]
    assert list(exchange_validator.iter_errors(value))


@pytest.mark.parametrize('change', [
    {'operation': 'urn:uuid:00000000-0000-4000-8000-000000000001'},
    {'operation': 'willman://operation/koru.inspect_tasks/v1?ticket=42'},
    {'operation': 'willman://operation/koru.inspect_tasks/v1#fragment'},
    {'requestUrn': 'urn:koru:ticket:338'},
    {'contractDigest': 'stale-unbound-name'},
    {'effects': []}, {'effects': ['read', 'read']},
    {'authorizationGranted': True}, {'kind': 'done'},
    {'inputs': [{'urn': resource(3)['urn'], 'mediaType': 'application/json'}]},
])
def test_invalid_or_ambiguous_request_rejected(exchange_validator, change):
    value = exchange()
    value.update(change)
    assert list(exchange_validator.iter_errors(value))


@pytest.mark.parametrize('cursor', ['leaseRevision', 'fencingToken'])
@pytest.mark.parametrize('invalid', [0, -1, True, '1'])
def test_invalid_fence_shape_rejected(exchange_validator, cursor, invalid):
    value = exchange('result', True)
    value['admission'][cursor] = invalid
    assert list(exchange_validator.iter_errors(value))


def test_worker_done_cannot_mask_blocked_outcome(exchange_validator):
    value = exchange('result')
    value.update(outcome='blocked', outputs=[], reason='No tasks admitted')
    exchange_validator.validate(value)
    false_success = deepcopy(value)
    false_success['outcome'] = 'completed'
    assert list(exchange_validator.iter_errors(false_success))


def test_echoed_arguments_are_not_a_completion_result(exchange_validator):
    value = exchange('result')
    value['arguments'] = {'output_format': 'csv'}
    assert list(exchange_validator.iter_errors(value))


def test_blocked_result_cannot_claim_completion(exchange_validator):
    value = exchange('result', True)
    value.update(outcome='blocked', reason='Expired admission')
    assert list(exchange_validator.iter_errors(value))


def test_shape_does_not_authenticate_a_controller_or_current_cursor(exchange_validator):
    # Structurally valid untrusted references are deliberately not a grant.
    # Consumers must perform cross-message, resolver and live-controller checks.
    value = exchange('result', True)
    value['context']['repositoryRef'] = 'other/repository'
    value['admission']['fencingToken'] = 999
    exchange_validator.validate(value)
    specification = (ROOT / 'spec/SEMANTIC_NL_PLAN.md').read_text()
    assert 'JSON Schema cannot express this comparison' in specification
    assert 'before every write or execution' in specification

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
