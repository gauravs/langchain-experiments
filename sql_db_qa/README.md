# SQL Database QA

Ask questions from a sqlite db file. Implements [cookbook/sql_db_qa](https://github.com/langchain-ai/langchain/blob/master/cookbook/sql_db_qa.mdx).

## Setup

Requires:

1. docker + docker compose
2. make
3. sqlite3
4. OpenAI API key (optional)

```sh
export OPENAI_API_KEY=xxxx
```

## Usage - Ollama

Working example with phind-codellama. This is not working well for more complex questions.

```sh
❯ make ask-ollama QUESTION="who is the most prolific artist?"


> Entering new SQLDatabaseChain chain...
who is the most prolific artist?
SQLQuery:SELECT A.Name, COUNT(T.TrackId) AS NumberOfTracks
FROM Artist A
JOIN Album AR ON A.ArtistId = AR.ArtistId
JOIN Track T ON AR.AlbumId = T.AlbumId
GROUP BY A.Name
ORDER BY NumberOfTracks DESC
LIMIT 1;
SQLResult: [('Iron Maiden', 213)]
Answer:The most prolific artist is "Iron Maiden" with 213 tracks.
> Finished chain.
```

## Usage - OpenAI

```sh
❯ make ask QUESTION="how many songs does acdc have?"

> Entering new SQLDatabaseChain chain...
how many songs does acdc have?
SQLQuery:SELECT COUNT(*) FROM Track WHERE AlbumId IN (SELECT AlbumId FROM Album WHERE ArtistId = (SELECT ArtistId FROM Artist WHERE Name = 'AC/DC'))
SQLResult: [(18,)]
Answer:AC/DC has 18 songs.
> Finished chain.
```

```sh
❯ make ask QUESTION="list all composers for the band aerosmith"

> Entering new SQLDatabaseChain chain...
list all composers for the band aerosmith
SQLQuery:SELECT "Composer" FROM "Track" WHERE "AlbumId" IN (SELECT "AlbumId" FROM "Album" WHERE "ArtistId" IN (SELECT "ArtistId" FROM "Artist" WHERE "Name" = 'Aerosmith')) LIMIT 5
SQLResult: [('Steven Tyler, Joe Perry, Jack Blades, Tommy Shaw',), ('Steven Tyler, Joe Perry',), ('Steven Tyler, Joe Perry, Jim Vallance, Holly Knight',), ('Steven Tyler, Joe Perry, Desmond Child',), ('Steven Tyler, Joe Perry, Desmond Child',)]
Answer:Steven Tyler, Joe Perry, Jack Blades, Tommy Shaw, Jim Vallance, Holly Knight, Desmond Child
> Finished chain.
```

```sh
❯ make ask QUESTION="who is the most prolific artist?"

> Entering new SQLDatabaseChain chain...
who is the most prolific artist?
SQLQuery:SELECT "Artist"."Name", COUNT("Track"."TrackId") AS "Number of Tracks" FROM "Artist" INNER JOIN "Album" ON "Artist"."ArtistId" = "Album"."ArtistId" INNER JOIN "Track" ON "Album"."AlbumId" = "Track"."AlbumId" GROUP BY "Artist"."Name" ORDER BY "Number of Tracks" DESC LIMIT 1;
SQLResult: [('Iron Maiden', 213)]
Answer:Iron Maiden
> Finished chain.
```

```sh
❯ make ask QUESTION="what are other artists like aerosmith, you should use genres for matching similar artists, dont hardcode the genre and read it on the fly from the db. return only names as a numbered list and dont use any limits"

> Entering new SQLDatabaseChain chain...
what are other artists like aerosmith, you should use genres for matching similar artists, dont hardcode the genre and read it on the fly from the db. return only names as a numbered list and dont use any limits
SQLQuery:SELECT DISTINCT Artist.Name
FROM Artist
INNER JOIN Album ON Artist.ArtistId = Album.ArtistId
INNER JOIN Track ON Album.AlbumId = Track.AlbumId
INNER JOIN Genre ON Track.GenreId = Genre.GenreId
WHERE Genre.Name = (SELECT Genre.Name FROM Artist
INNER JOIN Album ON Artist.ArtistId = Album.ArtistId
INNER JOIN Track ON Album.AlbumId = Track.AlbumId
INNER JOIN Genre ON Track.GenreId = Genre.GenreId
WHERE Artist.Name = "Aerosmith")
AND Artist.Name != "Aerosmith"
ORDER BY Artist.Name
SQLResult: [('AC/DC',), ('Accept',), ('Alanis Morissette',), ('Alice In Chains',), ('Audioslave',), ('Creedence Clearwater Revival',), ('David Coverdale',), ('Deep Purple',), ('Def Leppard',), ('Dread Zeppelin',), ('Faith No More',), ('Foo Fighters',), ('Frank Zappa & Captain Beefheart',), ("Guns N' Roses",), ('Iron Maiden',), ('Jamiroquai',), ('Jimi Hendrix',), ('Joe Satriani',), ('Kiss',), ('Led Zeppelin',), ('Lenny Kravitz',), ('Marillion',), ('Men At Work',), ('Nirvana',), ('O Terço',), ('Ozzy Osbourne',), ('Page & Plant',), ("Paul D'Ianno",), ('Pearl Jam',), ('Pink Floyd',), ('Queen',), ('R.E.M.',), ('Raul Seixas',), ('Red Hot Chili Peppers',), ('Rush',), ('Santana',), ('Scorpions',), ('Skank',), ('Soundgarden',), ('Stone Temple Pilots',), ('Terry Bozzio, Tony Levin & Steve Stevens',), ('The Cult',), ('The Doors',), ('The Police',), ('The Posies',), ('The Rolling Stones',), ('The Who',), ('U2',), ('Van Halen',), ('Velvet Revolver',)]
Answer:1. AC/DC
2. Accept
3. Alanis Morissette
4. Alice In Chains
5. Audioslave
6. Creedence Clearwater Revival
7. David Coverdale
8. Deep Purple
9. Def Leppard
10. Dread Zeppelin
11. Faith No More
12. Foo Fighters
13. Frank Zappa & Captain Beefheart
14. Guns N' Roses
15. Iron Maiden
16. Jamiroquai
17. Jimi Hendrix
18. Joe Satriani
19. Kiss
20. Led Zeppelin
21. Lenny Kravitz
22. Marillion
23. Men At Work
24. Nirvana
25. O Terço
26. Ozzy Osbourne
27. Page & Plant
28. Paul D'Ianno
29. Pearl Jam
30. Pink Floyd
31. Queen
32. R.E.M.
33. Raul Seixas
34. Red Hot Chili Peppers
35. Rush
36. Santana
37. Scorpions
38. Skank
39. Soundgarden
40. Stone Temple Pilots
41. Terry Bozzio, Tony Levin &
> Finished chain.
```
