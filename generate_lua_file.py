import os

uploaded_urls = sys.argv[1:]

if not uploaded_urls:
    print("No uploaded URLs provided.")
    sys.exit(1)

output_filename = "final_lua_script.lua"

os.makedirs("/tmp/output", exist_ok=True)

with open(f"/tmp/output/{output_filename}", 'w') as f:
    for url in uploaded_urls:
        f.write(url + "\n")

print(f"Lua script saved to /tmp/output/{output_filename}")
