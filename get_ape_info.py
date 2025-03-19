from web3 import Web3
from web3.providers.rpc import HTTPProvider
import requests
import json

bayc_address = "0xBC4CA0EdA7647A8aB7C2061c2E118A18a936f13D"
contract_address = Web3.to_checksum_address(bayc_address)

# You will need the ABI to connect to the contract
# The file 'abi.json' has the ABI for the bored ape contract
# In general, you can get contract ABIs from etherscan
# https://api.etherscan.io/api?module=contract&action=getabi&address=0xBC4CA0EdA7647A8aB7C2061c2E118A18a936f13D
with open('ape_abi.json', 'r') as f:
    abi = json.load(f)

############################
# Connect to an Ethereum node
api_url = "https://beige-given-cow-334.mypinata.cloud"  # YOU WILL NEED TO PROVIDE THE URL OF AN ETHEREUM NODE
provider = HTTPProvider(api_url)
web3 = Web3(provider)


def get_ape_info(ape_id):
    assert isinstance(ape_id, int), f"{ape_id} is not an int"
    assert 0 <= ape_id, f"{ape_id} must be at least 0"
    assert 9999 >= ape_id, f"{ape_id} must be less than 10,000"

    data = {'owner': "", 'image': "", 'eyes': ""}

    # YOUR CODE HERE

    contract = web3.eth.contract(address=contract_address, abi=abi)
    
    # Get the current owner of the ape (token) using ownerOf.
    owner = contract.functions.ownerOf(ape_id).call()
    data['owner'] = owner
    
    # Get the token URI (metadata URI) for the ape.
    token_uri = contract.functions.tokenURI(ape_id).call()
    
    # Convert IPFS URI to an HTTP URL via a gateway.
    if token_uri.startswith("ipfs://"):
        token_uri_http = token_uri.replace("ipfs://", "https://beige-given-cow-334.mypinata.cloud/ipfs/")
    else:
        token_uri_http = token_uri
    
    # Fetch the metadata JSON from the IPFS gateway.
    response = requests.get(token_uri_http)
    if response.status_code != 200:
        raise Exception(f"Failed to fetch metadata from {token_uri_http}")
    metadata = response.json()
    
    # Extract the image URI from the metadata.
    image_uri = metadata.get("image", "")
    data['image'] = image_uri
    
    # Find the "Eyes" attribute from the attributes list.
    eyes = ""
    attributes = metadata.get("attributes", [])
    for attr in attributes:
        # Normalize trait type for robust matching.
        if attr.get("trait_type", "").lower() == "eyes":
            eyes = attr.get("value", "")
            break
    data['eyes'] = eyes
    
    return data