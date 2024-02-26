# Official Python SDK for [Original](https://getoriginal.com) API

## Table of Contents

- [Getting Started](#-getting-started)
- [Documentation](#-documentation)
  - [Initialization](#initialization)
  - [User](#user)
  - [Asset](#asset)
  - [Collection](#collection)
  - [Transfer](#transfer)
  - [Burn](#burn)
  - [Deposit](#deposit)


## ✨ Getting started

Ensure you have registered for an account at [Original](https://app.getoriginal.com) before getting started.
You will need to create an app and note down your API key and secret from the [API Keys page](https://docs.getoriginal.com/docs/create-your-api-key) to use the Original SDK.

Install Original

```bash
$ pip install original-sdk
```

## 📚 Documentation

### Initialization

The Original SDK is set up to expose the Original API.

Read the full [Original API documentation](https://docs.getoriginal.com).


Create a new instance of the Original client by passing in your api key and secret, with the environment associated with that app.

### Development
For development apps, you must pass the environment:

```python
from original_sdk import OriginalClient, Environment

client = OriginalClient(api_key='YOUR_DEV_APP_API_KEY', api_secret='YOUR_DEV_APP_SECRET', env=Environment.Development)
```

### Production
For production apps, you can optionally pass the production environment:

```python
from original_sdk import OriginalClient, Environment

client = OriginalClient(api_key='YOUR_PROD_APP_API_KEY', api_secret='YOUR_PROD_APP_SECRET', env=Environment.Production)
```

or omit the environment, which will default to production:

```python
from original_sdk import OriginalClient

client = OriginalClient(api_key='YOUR_PROD_APP_API_KEY', api_secret='YOUR_PROD_APP_SECRET')
```


### User

The user methods exposed by the sdk are used to create and retrieve users from the Original API.

```python
# create a new user
new_user_uid = client.create_user(email='YOUR_EMAIL', client_id='YOUR_CLIENT_ID' )

# gets a user by uid, will throw a 404 Not Found error if the user does not exist
# returns user data
user = client.get_user(new_user_uid)

# gets a user by email or client_id
# will return user data type if the user exists, otherwise will return null
user_by_email = client.get_user_by_email('YOUR_EMAIL')

user_by_client_id = client.get_user_by_client_id('YOUR_CLIENT_ID')
```

### Asset

The asset methods exposed by the sdk are used to create (mint) assets and retrieve assets from the Original API.

```python
# prepare the new asset params
new_asset_data = {
    "user_uid": "324167489835",
    "client_id": "client_id_1",
    "collection_uid": "221137489875",
    "data": {
        "name": "Dave Starbelly",
        "unique_name": True,
        "image_url": "https://storage.googleapis.com/opensea-prod.appspot.com/puffs/3.png",
        "store_image_on_ipfs": True,
        "description": "Friendly OpenSea Creature that enjoys long swims in the ocean.",
        "external_url": "https://openseacreatures.io/3",
        "attributes": [
            {
                "trait_type": "Base",
                "value": "Starfish"
            },
            {
                "trait_type": "Eyes",
                "value": "Big"
            },
            {
                "trait_type": "Aqua Power",
                "display_type": "boost_number",
                "value": 40
            },
            {
                "trait_type": "Stamina Increase",
                "display_type": "boost_percentage",
                "value": 10
            },
        ]
    }
}

# create a new asset
# returns the uid of the newly created asset
new_asset_uid = client.create_asset(**new_asset_data)

# gets an asset by uid, will throw a 404 Not Found error if the asset does not exist
asset = client.get_asset(new_asset_uid)

# gets assets by the owner uid
# will return a list of assets owned by the user
assets = client.get_asset_by_user_uid(user_uid)

# prepare the edit asset params
edit_asset_data = {
    "data": {
        "name": "Dave Starbelly Edited",
        "unique_name": True,
        "image_url": "https://storage.googleapis.com/opensea-prod.appspot.com/puffs/3.png",
        "description": "Friendly OpenSea Creature that enjoys long swims in the ocean. Edited",
        "attributes": [
            {
                "trait_type": "Base",
                "value": "Starfish"
            },
        ]
    }
}

# edits an asset by uid, by passing in the new asset data
# returns success true or false
client.edit_asset(new_asset_uid, **edit_asset_data)
```

### Collection

The collection methods exposed by the sdk are used to retrieve collection details from the Original API.

```python
# gets a collection by uid, will throw a 404 Not Found error if the collection does not exist
# returns collection detail
collection = client.get_collection('221137489875')
```

### Transfer

The transfer methods exposed by the sdk are used to transfer assets from one user to another wallet.

```python

# prepare the transfer params
transfer_params = {
    "asset_uid": asset_uid,
    "from_user_uid": user_uid,
    "to_address": "0xd8dA6BF26964aF9D7eEd9e03E53415D37aA96045"
}

# create a transfer of an asset, by passing in transfer details
# returns the uid of the newly created transfer
transfer_uid = client.create_transfer(**transfer_params)

# gets a transfer by uid, will throw a 404 Not Found error if the transfer does not exist
transfer = client.get_transfer(transfer_uid)

# gets transfers by user uid
# will return a list of transfers for the user
transfers = client.get_transfers_by_user_uid(user_uid)
```

### Burn

The burn methods exposed by the sdk are used to burn assets from a user's wallet.

```python

# prepare the burn params
burn_params = {
    "asset_uid": asset_uid,
    "from_user_uid": user_uid,
}

# create a burn of an asset
# returns the uid of the newly created burn
burn_uid = client.create_burn(**burn_params)

# gets a burn by uid, will throw a 404 Not Found error if the burn does not exist
burn = client.get_burn(burn_uid)

# gets burns by user uid
burns = client.get_burn_by_user_uid(user_uid)
```


### Deposit

The deposit methods exposed by the sdk are used to return the details for depositing assets.

```python
# gets deposit details for a user
# returns the deposit details
deposit = client.get_deposit(user_uid)
```


### Handling Errors

If something goes wrong, you will receive well typed error messages.

```python
class ClientError(OriginalError): ...
class ServerError(OriginalError): ...
class ValidationError(OriginalError): ...
```

All errors inherit from an `OriginalError` class where you can access the standard properties from the `Exception` class as well as the following:

```python
class OriginalErrorCode(Enum):
    client_error = "client_error"
    server_error = "server_error"
    validation_error = "validation_error"
    

class OriginalError(Exception):
    def __init__(self, message, status, data, code):
        self.message = message
        self.status = status
        self.data = data
        self.code = code.value # 'client_error' | 'server_error' | 'validation_error'
}
```

So when an error occurs, you can either catch all using the OriginalError class:

```python
from original_sdk import OriginalError

try:
    result = client.create_user('invalid_email', 'client_id');
except OriginalError as e:
    # handle all errors
```

or specific errors:

```python
from original_sdk import ClientError, ServerError, ValidationError

try:
    result = client.create_user('invalid_email', 'client_id');
except ClientError as e:
    # handle client errors
except ServerError as e:
    # handle server errors
except ValidationError as e:
    # handle validation errors
```

The error will have this structure:
```python
except OriginalError as error:
    # error.code == 'client_error' | 'server_error' | 'validation_error'
    # error.status == 400 | 404 | ...
    # error.message == 'Not Found' | 'Enter a valid email address.' | ...
    # error.data == { 
    #   "success": False, 
    #   "error": { 
    #       "type": "validation_error", 
    #       "detail": { 
    #           "code": "invalid",
    #           "message": "Enter a valid email address.",
    #           "field_name": "email"
    #        }  
    #    }
    # }
```

Please note, if you plan to parse the error detail, it can also be an array if there are multiple errors.
```python
    # ...
    # "detail": [
    #     {
    #         "code": "null",
    #         "message": "This field may not be null.",
    #         "field_name": "client_id"
    #     },
    #     {
    #         "code": "invalid",
    #         "message": "Enter a valid email address.",
    #         "field_name": "email"
    #     }
    # ]
```

If it's a client (SDK) error and not a json response error from our server/REST API, we will return data as a string.
```python
    # "error.data": "Not Found"
    # "error.status": 404
    # "error.code": "client_error"
```
