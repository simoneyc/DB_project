import tkinter as tk
from tkinter import ttk
import mysql.connector

movie_list = []

# Connect to your MySQL database
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="4110056030",
    database="movie"
)

# Create a cursor object to interact with the database
cursor = db.cursor()

def get_selected_data():
    selected_option_1 = option_var_1.get()
    selected_option_2 = option_var_2.get()

    # Execute a query based on the selected option
    query = f"SELECT * FROM {selected_option_2} WHERE title = '{selected_option_1}';"
    cursor.execute(query)
    data = cursor.fetchall()
    # movie_list = [item[0] for item in data]
    for i in range(len(data)):
        print(data[i])


    # Display the data in the text widget
    display_text.delete(1.0, tk.END)  # Clear previous content
    for row in data:
        display_text.insert(tk.END, f"{row}\n")

# 建視窗
window = tk.Tk()
window.title("Database Viewer")


# 選單1
options_1 = ["The Shawshank Redemption", "The Godfather", "The Dark Knight", "The Godfather: Part II", "12 Angry Men", "Schindler's List", "The Lord of the Rings: The Return of the King", "Pulp Fiction", "The Lord of the Rings: The Fellowship of the Ring", "Il Buono, il brutto, il cattivo.", "Forrest Gump", "Fight Club", "The Lord of the Rings: The Two Towers", "Inception", "Star Wars: Episode V - The Empire Strikes Back", "The Matrix", "Goodfellas", "One Flew Over the Cuckoo's Nest", "Se7en", "It's a Wonderful Life", "Shichinin no samurai", "Interstellar", "The Silence of the Lambs", "Saving Private Ryan", "Cidade de Deus", "La Vita è bella", "The Green Mile", "Spider-Man: Across the Spider-Verse", "Star Wars", "Terminator 2: Judgment Day", "Back to the Future", "Sen to Chihiro no kamikakushi", "The Pianist", "Psycho", "Gisaengchung", "Gladiator", "The Lion King", "Léon", "American History X", "The Departed", "Whiplash", "The Prestige", "The Usual Suspects", "Hotaru no haka", "Seppuku", "Casablanca", "Intouchables", "Modern Times", "Nuovo cinema Paradiso", "C'era una volta il West", "Rear Window", "Alien", "City Lights", "Apocalypse Now", "Django Unchained", "Memento", "Raiders of the Lost Ark", "WALL·E", "Das Leben der Anderen", "Oppenheimer", "Sunset Blvd.", "Paths of Glory", "Avengers: Infinity War", "The Shining", "Spider-Man: Into the Spider-Verse", "The Great Dictator", "Witness for the Prosecution", "Aliens", "Inglourious Basterds", "The Dark Knight Rises", "American Beauty", "Dr. Strangelove or: How I Learned to Stop Worrying and Love the Bomb", "Oldeuboi", "Coco", "Amadeus", "Toy Story", "Das Boot", "Braveheart", "Avengers: Endgame", "Joker", "Mononoke-hime", "Good Will Hunting", "Kimi no na wa", "Once Upon a Time in America", "Tengoku to jigoku", "3 Idiots", "Singin' in the Rain", "Capharna?m", "Requiem for a Dream", "Idi i smotri", "Toy Story 3", "Star Wars: Episode VI - Return of the Jedi", "Eternal Sunshine of the Spotless Mind", "2001: A Space Odyssey", "Jagten", "Reservoir Dogs", "Ikiru", "Lawrence of Arabia", "The Apartment", "Citizen Kane", "M", "North by Northwest", "Vertigo", "Double Indemnity", "Le fabuleux destin d'Amélie Poulain", "Scarface", "Full Metal Jacket", "Incendies", "A Clockwork Orange", "Heat", "Up", "To Kill a Mockingbird", "Hamilton", "The Sting", "Jodaeiye Nader az Simin", "Indiana Jones and the Last Crusade", "Metropolis", "Die Hard", "Taare Zameen Par", "Snatch.", "Ladri di biciclette", "L.A. Confidential", "Taxi Driver", "1917", "Der Untergang", "Dangal", "Per qualche dollaro in più", "Batman Begins", "Top Gun: Maverick", "Some Like It Hot", "The Kid", "The Wolf of Wall Street", "The Father", "Green Book", "All About Eve", "Judgment at Nuremberg", "The Truman Show", "There Will Be Blood", "Casino", "Shutter Island", "Ran", "El Laberinto del fauno", "Jurassic Park", "The Sixth Sense", "Unforgiven", "A Beautiful Mind", "No Country for Old Men", "Yojimbo", "The Treasure of the Sierra Madre", "Kill Bill: Vol. 1", "The Thing", "Monty Python and the Holy Grail", "The Great Escape", "Finding Nemo", "Rash?mon", "The Elephant Man", "Chinatown", "Hauru no ugoku shiro", "Dial M for Murder", "Gone with the Wind", "V for Vendetta", "Prisoners", "Raging Bull", "Lock, Stock and Two Smoking Barrels", "El secreto de sus ojos", "Inside Out", "Spider-Man: No Way Home", "Three Billboards Outside Ebbing, Missouri", "Trainspotting", "The Bridge on the River Kwai", "Fargo", "Warrior", "Catch Me If You Can", "Gran Torino", "Klaus", "Tonari no Totoro", "Million Dollar Baby", "Harry Potter and the Deathly Hallows: Part 2", "Bacheha-Ye aseman", "Blade Runner", "12 Years a Slave", "Before Sunrise", "The Grand Budapest Hotel", "Ben-Hur", "The Gold Rush", "Barry Lyndon", "Gone Girl", "Hacksaw Ridge", "In the Name of the Father", "On the Waterfront", "Salinui chueok", "The General", "The Deer Hunter", "Smultronst?llet", "Relatos salvajes", "The Third Man", "Dead Poets Society", "Le Salaire de la peur", "Sherlock Jr.", "Mad Max: Fury Road","Monsters, Inc.", "Mr. Smith Goes to Washington", "Jaws", "How to Train Your Dragon", "Mary and Max", "Ford v Ferrari", "Det Sjunde inseglet", "Room", "The Big Lebowski", "Ratatouille", "Tokyo monogatari", "Rocky", "Hotel Rwanda", "Logan", "Spotlight", "Platoon", "La Passion de Jeanne d'Arc", "The Terminator", "Jai Bhim", "Before Sunset", "Rush", "Network", "The Best Years of Our Lives", "The Exorcist", "Stand by Me", "La Haine", "Pirates of the Caribbean: The Curse of the Black Pearl", "The Wizard of Oz", "The Incredibles", "Into the Wild", "Hachi: A Dog's Tale", "To Be or Not to Be", "Ah-ga-ssi", "Babam Ve Oglum", "La battaglia di Algeri", "Groundhog Day", "The Grapes of Wrath", "Amores perros", "The Sound of Music", "Rebecca", "Cool Hand Luke", "The Iron Giant", "Pather Panchali", "It Happened One Night", "The Help", "Les Quatre cents coups", "Aladdin", "Dances with Wolves", "Life of Brian", "Gangs of Wasseypur"]  # Replace with your actual table names
option_var_1 = tk.StringVar(window)
option_var_1.set(options_1[0])  # default選項

table_label_1 = tk.Label(window, text="選擇movie:",font=("Arial",16),fg="#2894FF")
table_label_1.pack(pady=10,side="left")


table_menu_1 = ttk.Combobox(window, textvariable=option_var_1, values=options_1,font=("Arial",16))
table_menu_1.pack(side="left")



# 選單2
options_2 = ["movieinfo", "boxoffice", "award","product","actor"]  # Replace with your actual table names
option_var_2 = tk.StringVar(window)
option_var_2.set(options_2[0])  # default選項

table_label_2 = tk.Label(window, text="選擇table:",font=("Arial",16),fg="#2894FF")
table_label_2.pack(pady=10)

table_menu_2 = ttk.Combobox(window, textvariable=option_var_2, values=options_2,font=("Arial",16))
table_menu_2.pack(side="left")

# Button to fetch and display data
fetch_button = tk.Button(window, text="確定", command=get_selected_data,font=("Arial",16),bg="purple",fg="white")
fetch_button.pack(pady=10)

# Text widget to display the selected data
display_text = tk.Text(window, height=1920, width=1080)
display_text.pack(pady=10)

# Start the Tkinter event loop
window.mainloop()

# Close the database connection when the application is closed
db.close()
