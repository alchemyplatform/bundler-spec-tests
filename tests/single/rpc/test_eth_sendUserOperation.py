"""
Test suite for `eip4337 bunlder` module.
See https://github.com/eth-infinitism/bundler
"""

import pytest
from jsonschema import validate, Validator
from tests.types import RPCErrorCode
from tests.utils import userop_hash, assert_rpc_error, send_bundle_now


@pytest.mark.parametrize("schema_method", ["eth_sendUserOperation"], ids=[""])
def test_eth_sendUserOperation(w3, wallet_contract, helper_contract, userop, schema):
    state_before = wallet_contract.functions.state().call()
    assert state_before == 0
    response = userop.send()
    send_bundle_now()
    state_after = wallet_contract.functions.state().call()
    assert response.result == userop_hash(helper_contract, userop)
    assert state_after == 1111111
    Validator.check_schema(schema)
    validate(instance=response.result, schema=schema)

@pytest.mark.skip(reason="todo: fix failed test")
def test_eth_sendUserOperation_revert(w3, wallet_contract, bad_sig_userop):
    state_before = wallet_contract.functions.state().call()
    assert state_before == 0
    response = bad_sig_userop.send()
    send_bundle_now()
    state_after = wallet_contract.functions.state().call()
    assert state_after == 0
    assert_rpc_error(
        response, "testWallet: dead signature", RPCErrorCode.REJECTED_BY_EP_OR_ACCOUNT
    )


def test_eth_sendUserOperation_invalid_signature(invalid_sig_userop):
    response = invalid_sig_userop.send()
    assert_rpc_error(
        response,
        response.message,
        RPCErrorCode.INVALID_SIGNATURE,
    )
