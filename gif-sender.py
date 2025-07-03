import os
import sys

os.makedirs("/tmp/output", exist_ok=True)

uploaded_urls = sys.argv[1:]

if not uploaded_urls:
    sys.exit(1)

output_filename = "output_lua_urls"

max_retries = 5
retry_delay = 1
success = False

for attempt in range(max_retries):
    try:
        with open(f"{os.path.join('/tmp/output', output_filename)}.lua", 'w') as f:
            for url in uploaded_urls:
                f.write(url + "\n")
        print("Processed uploaded URLs successfully.")
        success = True
        break
    except Exception as e:
        print(f"Error processing uploaded URLs: {e}")
        if attempt < max_retries - 1:
            print(f"Retrying in {retry_delay} seconds...")
            time.sleep(retry_delay)
        else:
            print(f"Failed to process after {max_retries} attempts.")

if success:
    print("All URLs processed successfully!")
else:
    print("Some files could not be processed after multiple attempts.")
