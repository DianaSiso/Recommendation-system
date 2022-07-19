import pandas as p
from collections import Counter

# returning distance based similarity between user_1 and user_2 using Euclidean distance score
def euclidean_distance(dictionary,user_1,user_2):
    similar = 0
    for x in dictionary[user_1]:
        if x in dictionary[user_2]:
            print(x)
            print(dictionary[user_1][x])
            similar += pow(dictionary[user_1][x] - dictionary[user_2][x],2) 
    if similar == 0: 
        return 0   
    return 1/(1+similar)

# getting best 10 users using Euclidean distance score
def get_users(dictionary, user, n=10, similarity = euclidean_distance):
    scores = []
    for other_user in dictionary:
        if other_user != user:
            scores.append((similarity(dictionary,user,other_user), other_user))
    scores.sort()
    scores.reverse()
    return scores[0:n]

# getting best 10 recommendations using Euclidean distance score
def get_recommendations(dictionary, user, n=10, similarity = euclidean_distance):
    total = {} 
    similar = {}
    rankings = []
    for other_user in dictionary:
        if other_user == user:
            continue
        sim = similarity(dictionary, user, other_user)
        if sim == 0:
            continue
        for x in dictionary[other_user]:
            if x not in dictionary[user]:
                total.setdefault(x,0) 
                similar.setdefault(x,0)
                total[x] += dictionary[other_user][x] * sim
                similar[x] += sim
    print(total)
    print(similar)
    for book, t in total.items():
        rankings.append((t/similar[book]/5.0, book))             
    rankings.sort()
    rankings.reverse()
    return rankings[0:n]


# importing and merging data
books = p.read_csv('../datasets/books.csv')
ratings = p.read_csv('../datasets/ratings.csv')
books_ratings = p.merge(books, ratings)

# considering only users that reviewed at least 20 books
books_ratings['number_of_reviews'] = books_ratings['user_id'].groupby(ratings['user_id']).transform('count') 
books_ratings = books_ratings.loc[(books_ratings['number_of_reviews'] >= 20)]
books_ratings = books_ratings.filter(items=['user_id', 'title', 'rating'])


# analysing data
# checking how many times the book was rated
print(Counter(books_ratings['title']))

# checking how many times different users rated the same book
print(books_ratings.groupby('title')['user_id'].unique())

# converting dataframe to dict
d = (books_ratings.groupby('user_id')[['title','rating']].apply(lambda x: dict(x.values)).to_dict())

# top 10 similar users to user id 3
print(get_users(d, 3))

# top recommendation for user id 3
print(get_recommendations(d, 3))

