# Setup and Installation

## Step 1

Clone the repository. Then run `pipenv shell .`

## Step 2

To make sure Earth Engine API is configured with your Google Drive, do the following:

```bash
# reference: https://geoscripting-wur.github.io/Earth_Engine/
# Install earthengine-api
pip install earthengine-api

# Authenticate earth engine
earthengine authenticate
# Follow procedure to authenticate and paste the access token in your terminal

# Check if earth engine has been installed
python -c "import ee; ee.Initialize()"
# If you don't get an error, you are good to go
```

\\[ x = {-b \pm \sqrt{b^2-4ac} \over 2a} \\]
