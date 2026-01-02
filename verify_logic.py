from recommender import get_book_titles, recommend_by_title, get_trending

print("Testing get_book_titles...")
titles = get_book_titles()
print(f"Success! Retrieved {len(titles)} titles. First 3: {titles[:3]}")

print("\nTesting get_trending...")
trending = get_trending(5)
print("Success! Trending columns:", trending.columns.tolist())

print("\nTesting recommend_by_title...")
# Use a known title
test_title = titles[0]
print(f"Getting recommendations for '{test_title}'...")
recs = recommend_by_title(test_title)
if recs is not None and not recs.empty:
    print("Success! Recommendations found.")
    print(recs.head(2))
else:
    print("Warning: No recommendations found (might be expected for some books).")
