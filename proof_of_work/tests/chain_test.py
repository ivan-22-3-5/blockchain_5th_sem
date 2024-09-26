from tests.fixtures import keys, chain, block, transactions, sender_and_recipient


def test_initial_chain(chain):
    assert len(chain._chain) == 1
    assert chain.get_last_block().previous_hash == "none"


def test_add_block(chain, block, keys):
    private_key, public_key = keys
    chain.add_block(public_key, block.sign(private_key))
    assert len(chain._chain) == 2


def test_get_block(chain, block, keys):
    private_key, public_key = keys
    chain.add_block(public_key, block.sign(private_key))
    assert chain.get_block(1) == block


def test_get_block_invalid_index(chain):
    assert chain.get_block(100) is None
    assert chain.get_block(-1) is None


def test_get_last_block(chain, block, keys):
    private_key, public_key = keys
    chain.add_block(public_key, block.sign(private_key))
    assert chain.get_last_block() == block
