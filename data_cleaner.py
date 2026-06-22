import json
import pandas as pd

# List of your JSON files
json_files = ['PokemonRomhacks1st100.json', 'PokemonRomhacks2nd100.json', 'PokemonRomhacks3rd100.json', 'PokemonRomhacks4th100.json', 'PokemonRomhacks5th100.json', 'PokemonRomhacks6th100.json', 'PokemonRomhacks7th100.json']

# List to store all extracted post data
all_posts = []

for file_name in json_files:
    try:
        with open(file_name, 'r', encoding='utf-8') as f:
            data = json.load(f)
            
            posts_list = data.get('data', {}).get('children', [])
            
            for post in posts_list:
                post_data = post.get('data', {})
                
                # Extract fields
                title = post_data.get('title')
                post_text = post_data.get('selftext')
                link_flair_text = post_data.get('link_flair_text')
                post_url = post_data.get('url')  # <--- Extract the link here
                
                # Apply your flair filter
                if link_flair_text in ['Review', 'Discussion', 'Development', 'Release'] and post_text is not "":
                    all_posts.append({
                        'title': title,
                        'link_flair_text': link_flair_text,
                        'post_url': post_url,
                        'post_text': post_text
                    })
                
    except FileNotFoundError:
        print(f"Warning: {file_name} not found.")
    except json.JSONDecodeError:
        print(f"Error: {file_name} is not a valid JSON.")

print(f"Successfully filtered {len(all_posts)} posts.\n")

# Save to CSV
if all_posts:
    df = pd.DataFrame(all_posts)
    df.to_csv('extracted_pokemon_posts.csv', index=False, encoding='utf-8')
    print("✓ Saved with URLs to 'extracted_pokemon_posts.csv'")

# Save to JSON
if all_posts:
    with open('extracted_pokemon_posts.json', 'w', encoding='utf-8') as out_f:
        json.dump(all_posts, out_f, indent=4, ensure_ascii=False)
        print("✓ Saved with URLs to 'extracted_pokemon_posts.json'")