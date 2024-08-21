from pathlib import Path
from datetime import date
import csv
import random
from faker import Faker

from django.contrib.auth.models import User
from apps.reader.models import Reader, NIC
from apps.book.models import Book, BookAuthor, Author, Tag
from apps.myread.models import MyRead, StatusPercent

# initialize Faker
fake = Faker()

# Create a directory 'csv' in the current directory
csv_file_path = Path('csv')
csv_file_path.mkdir()


def save_to_csv(csv_file, data):
    # Save in csv file
    writer = csv.writer(csv_file)
    data_key_list = list(data)
    limit = len(list(data.values())[0])
    writer.writerow(data.keys())
    for i in range(limit):
        writer.writerow(data[x][i] for x in data_key_list)


#################################
#         READER
#################################

# USER
users = None

# Open the csv file to save data as well
with open(csv_file_path / 'user.csv', 'w') as csv_file:
    # Generate 10 users
    data = {
        "username": [fake.user_name() for _ in range(10)],
        "first_name": [fake.first_name() for _ in range(10)],
        "last_name": [fake.last_name() for _ in range(10)],
        "email": [fake.email() for _ in range(10)],
        "password": [fake.password() for _ in range(10)]
    }
    
    # save to csv file
    save_to_csv(csv_file, data)
    # add to users list
    users = data


print('USER SAVED ON CSV....')
# NIC
nics = None
with open(csv_file_path / 'nic.csv', 'w') as csv_file:
    data = {
        "nic_number": [nic[:10] for nic in fake.nic_handles(10)],
        "delivery_date": [fake.date() for _ in range(10)]
    }

    save_to_csv(csv_file, data)
    nics = data

print('NIC SAVED ON CSV....')

# Save USER
for i in range(10):
    user = User(
        username=users['username'][i],
        first_name = users['first_name'][i],
        last_name=users['last_name'][i],
        email=users['email'][i]
    )
    user.set_password(users['password'][i])
    user.save()

print('USER SAVED ON DB....')
# Save NIC
for i in range(10):
    NIC.objects.get_or_create(
        nic_number=nics['nic_number'][i],
        delivery_date = nics['delivery_date'][i]
    )

print('NIC SAVED ON DB....')

# READER
readers = None
with open(csv_file_path / 'reader.csv', 'w') as csv_file:
    # Generate 10 readers
    user_pk = list(User.objects.all().values_list('id', flat=True))
    nic_pk = list(NIC.objects.all().values_list('nic_number', flat=True))
    fake.random.shuffle(user_pk)
    fake.random.shuffle(nic_pk)
    data = {
        "user": user_pk,
        "title": [fake.random.choice(['Mr', 'Mrs', 'Ms', 'Dr']) for _ in range(10)],
        "nic": nic_pk,
    }
    # save to csv file
    save_to_csv(csv_file, data)
    # add to users list
    readers = data

print('READER SAVED ON CSV....')

# Save READER
readers_ids = []
for i in range(10):
    user = User.objects.get(pk=readers['user'][i])
    nic = NIC.objects.get(pk=readers['nic'][i])
    reader, _ = Reader.objects.get_or_create(
        user=user,
        title=readers['title'][i],
        nic=nic
    )
    readers_ids.append(reader.pk)

print('READER SAVED ON DB....')
# # ##############################
# # #          BOOK
# # #############################

# AUTHOR
authors = None 
with open(csv_file_path / 'author.csv', 'w') as csv_file:
    # Generate 30 authors
    data = {
        "first_name": [fake.first_name() for _ in range(30)],
        "last_name": [fake.last_name() for _ in range(30)],
    }
    
    # save to csv file
    save_to_csv(csv_file, data)
    # add to users list
    authors = data

print('AUTHOR SAVED ON CSV....')
# TAG
tags = None 
with open(csv_file_path / 'tags.csv', 'w') as csv_file:
    # Generate 8 tags
    data = {
        "name": ['data science', 'python', 'art', 'data', 'money', 'love', 'movie', 'atom']
    }
    
    # save to csv file
    save_to_csv(csv_file, data)
    # add to users list
    tags = data

print('TAG SAVED ON CSV....')
# Save TAG and AUTHOR
authors_ids = []
for i in range(30):
    author, _ = Author.objects.get_or_create(
        first_name = authors['first_name'][i],
        last_name = authors['last_name'][i]
    )
    authors_ids.append(author.pk)
    
print('AUTHOR SAVED ON DB....')
tags_ids = []
for i in range(8):
    tag, _ = Tag.objects.get_or_create(
        name=tags['name'][i]
    )
    tags_ids.append(tag.pk)

print('TAG SAVED ON DB....')
# BOOK
books = None 
with open(csv_file_path / 'book.csv', 'w') as csv_file:
    # Generate 10 books
    data = {
        "isbn": [fake.isbn10() for _ in range(10)],
        "title": [fake.sentence()[:50] for _ in range(10)],
        "description": [''.join(fake.texts()) for _ in range(10)],
        "page_count": [random.randint(50, 500) for _ in range(10)],
        "category": [fake.random.choice(['pr', 'ar', 'hi', 'po', 'ot']) for _ in range(10)],
        "published_date": [int(fake.year()) for _ in range(10)],
        "publisher": [fake.company()[:50] for _ in range(10)],
        "lang": [fake.language_name()[:50] for _ in range(10)],
        "edition": [fake.random.choice([1,2,3]) for _ in range(10)],
        "book_format": [fake.random.choice(['eb', 'hc']) for _ in range(10)],
        "authors": [[a1, a2, a3] for a1, a2, a3 in [[
                    fake.random.choice(authors_ids),
                    fake.random.choice(authors_ids),
                    fake.random.choice(authors_ids)]]
                    for _ in range(10)],
        "tags": [[t1, t2, t3] for t1, t2, t3 in [[
            fake.random.choice(tags_ids),
            fake.random.choice(tags_ids),
            fake.random.choice(tags_ids)]]
            for _ in range(10)]
    }
    
    # save to csv file
    save_to_csv(csv_file, data)
    # add to users list
    books = data

print('BOOK SAVED ON CSV....')
# Save books
for i in range(10):
    book_tags = [Tag.objects.get(pk=tag_id) for tag_id in books['tags'][i]]
    book_authors = [Author.objects.get(pk=author_id ) for author_id in books['authors'][i]]

    book = Book(
        isbn=books['isbn'][i],
        title=books['title'][i],
        description=books['description'][i],
        page_count=books['page_count'][i],
        category=books['category'][i],
        published_date=books['published_date'][i],
        publisher=books['publisher'][i],
        lang=books['lang'][i],
        edition=books['edition'][i],
        book_format=books['book_format'][i],
    )
    book.save()
    book.tags.set(book_tags)
    for idx, author in enumerate(book_authors):
        BookAuthor.objects.get_or_create(
            book=book,
            author=author,
            role = 'author' if idx==0 else fake.random.choice(['co_author', 'editor'])
        )
print('BOOK SAVED ON DB....')


###############################
#          MYREAD
###############################
myreads = None 

with open(csv_file_path / 'myread.csv', 'w') as csv_file:
    # Generate 30 myreads
    percentage_read = [random.randint(0, 100) for _ in range(30)]
    start_read_date = [None if p_r == 0 else fake.date() for p_r in percentage_read]
    data = {
        "book_isbn":[books['isbn'][random.randint(0, 9)] for _ in range(30)],
        "reader_username":[readers_ids[random.randint(0, 9)] for _ in range(30)],
        "percentage_read": percentage_read,
        "start_read_date": start_read_date,
        "end_read_date":[fake.date_between_dates(date.fromisoformat(start)) if p_r == 100 else None  
                         for start, p_r in zip(start_read_date, percentage_read)]
    }

    # save to csv file
    save_to_csv(csv_file, data)
    # add to users list
    myreads = data

print('MYREAD SAVED ON CSV...')

for i in range(30):
    book = Book.objects.get(pk=myreads['book_isbn'][i])
    reader = Reader.objects.get(pk=myreads['reader_username'][i])
    MyRead.objects.get_or_create(
        book_isbn = book,
        reader_username = reader,
        percentage_read = myreads['percentage_read'][i],
        start_read_date = myreads['start_read_date'][i],
        end_read_date = myreads['end_read_date'][i]
    )

print('MYREAD SAVED ON DB...')

# STATUS PERCENT
for status, per_range in [('pending','[0,0]') , ('reading','[1,99]'), ('done', '[100,100]')]:
    StatusPercent.objects.get_or_create(
        read_status = status,
        percentage_read_range = per_range
    )

print('STATUS PERCENT SAVED TO DB...')