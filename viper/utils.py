import binascii
try:
    from Crypto.Hash import keccak
    sha3 = lambda x: keccak.new(digest_bits=256, data=x).digest()
except ImportError:
    import sha3 as _sha3
    sha3 = lambda x: _sha3.sha3_256(x).digest()

# Converts for bytes to an integer
def fourbytes_to_int(inp):
    return (inp[0] << 24) + (inp[1] << 16) + (inp[2] << 8) + inp[3]

# Converts a provided hex string to an integer
def hex_to_int(inp):
    if inp[:2] == '0x':
        inp = inp[2:]
    return bytes_to_int(binascii.unhexlify(inp))

# Converts bytes to an integer
def bytes_to_int(bytez):
    o = 0
    for b in bytez:
        o = o * 256 + b
    return o

# Encodes an address using ethereum's checksum scheme
def checksum_encode(addr): # Expects an input of the form 0x<40 hex chars>
    assert addr[:2] == '0x' and len(addr) == 42
    o = ''
    v = bytes_to_int(sha3(addr[2:].lower().encode('utf-8')))
    for i, c in enumerate(addr[2:]):
        if c in '0123456789':
            o += c
        else:
            o += c.upper() if (v & (2**(255 - 4*i))) else c.lower()
    return '0x'+o


# A decimal value can store multiples of 1/DECIMAL_DIVISOR
DECIMAL_DIVISOR = 10000000000

# Number of bytes in memory used for system purposes, not for variables
RESERVED_MEMORY = 320
ADDRSIZE_POS = 32
MAXNUM_POS = 64
MINNUM_POS = 96
MAXDECIMAL_POS = 128
MINDECIMAL_POS = 160
FREE_VAR_SPACE = 192
BLANK_SPACE = 224
FREE_LOOP_INDEX = 256

RLP_DECODER_ADDRESS = hex_to_int('0x84E7F44DdDc2Eaf6cdd08C18c80d1c4E15F99FF8'[2:])

# Instructions for creating RLP decoder on other chains
# First, Send 9366960000000000 wei to 0x0A51b02F77E7c8dc64962B9d5FdAb8D9eC6cfBbe
# Then, publish this TX to create the contract: 0xf903bf808506fc23ac008304c3a88080b903ac61039a8061000e6000396103a85660006101df5361202059905901600090526101008152602081019050602052600060605261040036018060200159905901600090528181526020810190509050608052600060e0527f0100000000000000000000000000000000000000000000000000000000000000600035046101005260c061010051121561007e57fe5b60f86101005112156100a95760c061010051036001013614151561009e57fe5b6001610120526100ec565b60f761010051036020036101000a600161012051013504610140526101405160f7610100510360010101361415156100dd57fe5b60f76101005103600101610120525b5b366101205112156102ec577f01000000000000000000000000000000000000000000000000000000000000006101205135046101005260e0516060516020026020510152600160605101606052608061010051121561017a57600160e0516080510152600161012051602060e0516080510101376001610120510161012052602160e0510160e0526102da565b60b8610100511215610218576080610100510360e05160805101526080610100510360016101205101602060e05160805101013760816101005114156101ef5760807f010000000000000000000000000000000000000000000000000000000000000060016101205101350412156101ee57fe5b5b600160806101005103016101205101610120526020608061010051030160e0510160e0526102d9565b60c06101005112156102d65760b761010051036020036101000a6001610120510135046101405260007f0100000000000000000000000000000000000000000000000000000000000000600161012051013504141561027357fe5b603861014051121561028157fe5b6101405160e05160805101526101405160b761010051600161012051010103602060e05160805101013761014051600160b7610100510301016101205101610120526020610140510160e0510160e0526102d8565bfe5b5b5b602060605113156102e757fe5b6100ed565b60e051606051602002602051015261082059905901600090526108008152602081019050610160526000610120525b6060516101205113151561035c576020602060605102610120516020026020510151010161012051602002610160510152600161012051016101205261031b565b60e051600a8105601201816020602060605102610160510101836080516000600486f161038557fe5b5050602060e051602060605102010161016051f35b6000f31b2d4f
