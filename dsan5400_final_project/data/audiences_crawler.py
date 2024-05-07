# Audiences Reviews
import asyncio
import csv
from pyppeteer import launch
import nest_asyncio

# Movie data including name, year, Oscar winning status, and review page URL
movies = [
    {"name": "Parasite", "year": "2020", "oscar": "Yes", "url": "https://www.rottentomatoes.com/m/parasite_2019/reviews?type=user"},
    {"name": "Ford v Ferrari", "year": "2020", "oscar": "No", "url": "https://www.rottentomatoes.com/m/ford_v_ferrari/reviews?type=user"},
    {"name": "The Irishman", "year": "2020", "oscar": "No", "url": "https://www.rottentomatoes.com/m/the_irishman/reviews?type=user"},
    {"name": "Jojo Rabbit", "year": "2020", "oscar": "No", "url": "https://www.rottentomatoes.com/m/jojo_rabbit/reviews?type=user"},
    {"name": "Joker", "year": "2020", "oscar": "No", "url": "https://www.rottentomatoes.com/m/joker_2019/reviews?type=user"},
    {"name": "Little Women", "year": "2020", "oscar": "No", "url": "https://www.rottentomatoes.com/m/little_women_2019/reviews?type=user"},
    {"name": "Marriage Story", "year": "2020", "oscar": "No", "url": "https://www.rottentomatoes.com/m/marriage_story_2019/reviews?type=user"},
    {"name": "1917", "year": "2020", "oscar": "No", "url": "https://www.rottentomatoes.com/m/1917_2019/reviews?type=user"},
    {"name": "Once Upon a Time in Hollywood", "year": "2020", "oscar": "No", "url": "https://www.rottentomatoes.com/m/once_upon_a_time_in_hollywood/reviews?type=user"},
    {"name": "Nomadland", "year": "2021", "oscar": "Yes", "url": "https://www.rottentomatoes.com/m/nomadland/reviews?type=user"},
    {"name": "Sound of Metal", "year": "2021", "oscar": "No", "url": "https://www.rottentomatoes.com/m/sound_of_metal/reviews?type=user"},
    {"name": "Mank", "year": "2021", "oscar": "No", "url": "https://www.rottentomatoes.com/m/mank/reviews?type=user"},
    {"name": "Minari", "year": "2021", "oscar": "No", "url": "https://www.rottentomatoes.com/m/minari/reviews?type=user"},
    {"name": "Promising Young Woman", "year": "2021", "oscar": "No", "url": "https://www.rottentomatoes.com/m/promising_young_woman/reviews?type=user"},
    {"name": "The Father", "year": "2021", "oscar": "No", "url": "https://www.rottentomatoes.com/m/the_father_2020/reviews?type=user"},
    {"name": "Judas and the Black Messiah", "year": "2021", "oscar": "No", "url": "https://www.rottentomatoes.com/m/judas_and_the_black_messiah/reviews?type=user"},
    {"name": "The Trial of the Chicago 7", "year": "2021", "oscar": "No", "url": "https://www.rottentomatoes.com/m/the_trial_of_the_chicago_7/reviews?type=user"},
    {"name": "CODA", "year": "2022", "oscar": "Yes", "url": "https://www.rottentomatoes.com/m/coda_2021/reviews?type=user"},
    {"name": "Nightmare Alley", "year": "2022", "oscar": "No", "url": "https://www.rottentomatoes.com/m/nightmare_alley_2021/reviews?type=user"},
    {"name": "Don't Look Up", "year": "2022", "oscar": "No", "url": "https://www.rottentomatoes.com/m/dont_look_up_2021/reviews?type=user"},
    {"name": "Dune: Part One", "year": "2022", "oscar": "No", "url": "https://www.rottentomatoes.com/m/dune_2021/reviews?type=user"},
    {"name": "Drive My Car", "year": "2022", "oscar": "No", "url": "https://www.rottentomatoes.com/m/drive_my_car/reviews?type=user"},
    {"name": "Belfast", "year": "2022", "oscar": "No", "url": "https://www.rottentomatoes.com/m/belfast/reviews?type=user"},
    {"name": "Licorice Pizza", "year": "2022", "oscar": "No", "url": "https://www.rottentomatoes.com/m/licorice_pizza/reviews?type=user"},
    {"name": "The Power of the Dog", "year": "2022", "oscar": "No", "url": "https://www.rottentomatoes.com/m/the_power_of_the_dog/reviews?type=user"},
    {"name": "West Side Story", "year": "2022", "oscar": "No", "url": "https://www.rottentomatoes.com/m/west_side_story_2021/reviews?type=user"},
    {"name": "King Richard", "year": "2022", "oscar": "No", "url": "https://www.rottentomatoes.com/m/king_richard/reviews?type=user"},
    {"name": "Everything Everywhere All at Once", "year": "2023", "oscar": "Yes", "url": "https://www.rottentomatoes.com/m/everything_everywhere_all_at_once/reviews?type=user"},
    {"name": "Top Gun: Maverick", "year": "2023", "oscar": "No", "url": "https://www.rottentomatoes.com/m/top_gun_maverick/reviews?type=user"},
    {"name": "Women Talking", "year": "2023", "oscar": "No", "url": "https://www.rottentomatoes.com/m/women_talking/reviews?type=user"},
    {"name": "The Banshees of Inisherin", "year": "2023", "oscar": "No", "url": "https://www.rottentomatoes.com/m/the_banshees_of_inisherin/reviews?type=user"},
    {"name": "Triangle of Sadness", "year": "2023", "oscar": "No", "url": "https://www.rottentomatoes.com/m/triangle_of_sadness/reviews?type=user"},
    {"name": "The Fabelmans", "year": "2023", "oscar": "No", "url": "https://www.rottentomatoes.com/m/the_fabelmans/reviews?type=user"},
    {"name": "All Quiet on the Western Front", "year": "2023", "oscar": "No", "url": "https://www.rottentomatoes.com/m/all_quiet_on_the_western_front_2022/reviews?type=user"},
    {"name": "Avatar: The Way of Water", "year": "2023", "oscar": "No", "url": "https://www.rottentomatoes.com/m/avatar_the_way_of_water/reviews?type=user"},
    {"name": "Elvis", "year": "2023", "oscar": "No", "url": "https://www.rottentomatoes.com/m/elvis/reviews?type=user"},
    {"name": "Tár", "year": "2023", "oscar": "No", "url": "https://www.rottentomatoes.com/m/tar_2022/reviews?type=user"},
    {"name": "Oppenheimer", "year": "2024", "oscar": "Yes", "url": "https://www.rottentomatoes.com/m/oppenheimer_2023/reviews?type=user"},
    {"name": "The Holdovers", "year": "2024", "oscar": "No", "url": "https://www.rottentomatoes.com/m/the_holdovers/reviews?type=user"},
    {"name": "American Fiction", "year": "2024", "oscar": "No", "url": "https://www.rottentomatoes.com/m/american_fiction/reviews?type=user"},
    {"name": "The Zone of Interest", "year": "2024", "oscar": "No", "url": "https://www.rottentomatoes.com/m/the_zone_of_interest/reviews?type=user"},
    {"name": "Barbie", "year": "2024", "oscar": "No", "url": "https://www.rottentomatoes.com/m/barbie/reviews?type=user"},
    {"name": "Poor Things", "year": "2024", "oscar": "No", "url": "https://www.rottentomatoes.com/m/poor_things/reviews?type=user"},
    {"name": "Past Lives", "year": "2024", "oscar": "No", "url": "https://www.rottentomatoes.com/m/past_lives/reviews?type=user"},
    {"name": "Anatomy of a Fall", "year": "2024", "oscar": "No", "url": "https://www.rottentomatoes.com/m/anatomy_of_a_fall/reviews?type=user"},
    {"name": "Maestro", "year": "2024", "oscar": "No", "url": "https://www.rottentomatoes.com/m/maestro_2023/reviews?type=user"},
    {"name": "Killers of the Flower Moon", "year": "2024", "oscar": "No", "url": "https://www.rottentomatoes.com/m/killers_of_the_flower_moon/reviews?type=user"}
]

async def scrape_reviews(movie):
    browser = await launch(headless=False)
    page = await browser.newPage()
    await page.goto(movie["url"])
    data_points = []
    review_count = 0  # Initialize review counter

    while True:
        # XPath to fetch review texts
        elements = await page.xpath('//drawer-more/p')
        # XPath to fetch review dates
        dates = await page.xpath('/html/body/div[3]/main/div/div/section/div/div[1]/div/div[2]/div[1]/span[2]')

        if not elements or review_count >= 20000:  # Stop if no more reviews or 1000 reviews are collected
            break

        for element, date_element in zip(elements, dates):
            if review_count >= 20000:
                break  # Stop collecting if the limit is reached
            text_content = await page.evaluate('(element) => element.textContent', element)
            date_content = await page.evaluate('(element) => element.textContent', date_element)
            data_points.append([movie["name"], movie["year"], movie["oscar"], text_content.strip(), date_content.strip()])
            review_count += 1  # Increment review counter

        try:
            load_more_button = await page.xpath('//rt-button')
            if not load_more_button or review_count >= 20000:
                break
            await load_more_button[0].click()
            await asyncio.sleep(2)
        except Exception as e:
            print(f"Error occurred: {e}")
            break

    await browser.close()
    return data_points

async def save_reviews_to_csv():
    with open('/Users/zhaoqianxue/Desktop/GU/24Spring/5400/Final/data/audiences_reviews.csv', 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['Movie Name', 'Year', 'Oscar Won', 'Review', 'Date'])
        for movie in movies:
            reviews = await scrape_reviews(movie)
            for review in reviews:
                writer.writerow(review)

# Apply nest_asyncio patch to handle event loop in interactive environments
nest_asyncio.apply()

# Run the async function to scrape and save reviews
asyncio.get_event_loop().run_until_complete(save_reviews_to_csv())