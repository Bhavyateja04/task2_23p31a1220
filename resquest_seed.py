import requests

student_id = "23p31a1220"
repo_url = "https://github.com/Bhavyateja04/task2_23p31a1220"

with open("student_public.pem", "r") as f:
    public_key = f.read()

payload = {
    "student_id": student_id,
    "github_repo_url": repo_url,
    "public_key": public_key
}

response = requests.post(
    "https://eajeyq4r3zljoq4rpovy2nthda0vtjqf.lambda-url.ap-south-1.on.aws",
    json=payload,
    timeout=15
)

data = response.json()
print("Response:", data)

if "encrypted_seed" in data:
    with open("encrypted_seed.txt", "w") as f:
        f.write(data["encrypted_seed"])
    print("\nEncrypted seed saved to encrypted_seed.txt")
else:
    print("\nERROR: encrypted_seed not returned!")
