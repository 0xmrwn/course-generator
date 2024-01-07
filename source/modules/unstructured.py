from unstructured_client import UnstructuredClient
from unstructured_client.models import shared
from unstructured_client.models.errors import SDKError

s = UnstructuredClient(api_key_auth="sSCxWPq8pswkM5mfDegThZHMfkrwn9")

filename = "courses/seconde/maths/Programme de mathématiques de seconde générale et technologique.pdf"
file = open(filename, "rb")

req = shared.PartitionParameters(
    # Note that this currently only supports a single file
    files=shared.Files(
        content=file.read(),
        file_name=filename,
    ),
    # Other partition params
    strategy="hi_res",
    hi_res_model_name="chipper",
    chunking_strategy="by_title",
    new_after_n_chars=2000,
)

try:
    res = s.general.partition(req)
except SDKError as e:
    print(e)

for element in res.elements:
    print("-------")
    print(element)
    print("-------")
