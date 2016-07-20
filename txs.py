from pycoin.services.blockchain_info import spendables_for_address
from pycoin.tx import script, Tx
from pycoin.tx.tx_utils import sign_tx
from pycoin.tx.TxOut import TxOut, standard_tx_out_script
from binascii import hexlify
from pycoin.serialize import b2h_rev
import json
import requests

def spendable_to_legible(spendable):
    return b2h_rev(spendable.previous_hash) + ":" + str(spendable.previous_index)

def write_opreturn(bitcoin_address, bitcoin_private_key, raw_message, fee=5000, push=False):
    message = hexlify(raw_message.encode()).decode('utf8')
    spendables = spendables_for_address(bitcoin_address)
    spendables = [s for s in spendables]
    bitcoin_sum = sum([spendable.coin_value for spendable in spendables])
    inputs = [spendable.tx_in() for spendable in spendables]
    outputs = []
    if (bitcoin_sum > fee):
        change_output_script = standard_tx_out_script(bitcoin_address)
        print change_output_script
        outputs.append(TxOut(bitcoin_sum - fee, change_output_script))

        ## Build the OP_RETURN output with our message
        op_return_output_script = script.tools.compile("OP_RETURN %s" % message)
        outputs.append(TxOut(0, op_return_output_script))

        ## Create the transaction and sign it with the private key
        tx = Tx(version=1, txs_in=inputs, txs_out=outputs)
        tx.set_unspents(spendables)
        sign_tx(tx, wifs=[bitcoin_private_key])
        print tx.as_hex()
        if not push:
            return tx.as_hex()
        else:
            pushtx(tx.as_hex())
    else:
        print "INADEQUATE FUNDS"

def pushtx(rawtx):
    url = "http://btc.blockr.io/api/v1/tx/push"
    data = {}
    data['hex'] = rawtx
    jsondata = json.dumps(data)
    print "PUSHING"
    print rawtx
    print ''
    response = requests.post(url, data=jsondata)
    print "Push Response was "+str(response.content) +" FROM BLOCKR"
    jsonresponse = json.loads(response.content)
    return str(jsonresponse['transaction_hash'])
