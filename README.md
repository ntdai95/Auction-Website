# Auctioneer

An auction marketplace split into six Flask REST services, each owning its own
datastore, so a schema change in one service cannot break the services that call it.
Five sit behind their own MySQL database and the messaging service uses MongoDB.
Messages travel between services over RabbitMQ. The whole thing runs as 14 Docker
containers on a shared bridge network.

Built at the University of Chicago in a team of four.

## Demo

Every screenshot below is the running stack in a browser at `localhost:3309`.

### Signing in

![Sign in](docs/01-login.png)

### Searching the catalogue

Search filters on item properties, so `categories:cameras` returns the items in that
category. Each result carries the actions that apply to it, including buying outright
and adding to a watchlist.

![Search results](docs/02-search.png)

### Listing what you own

Items you have added, with the option to open an auction on any of them.

![My items](docs/03-my-items.png)

### Bidding

The auction page shows the item, the auction type, whether it is live, and the highest
bid so far. The seller controls for closing an auction only render for an
administrator.

![An auction with a bid placed](docs/04-auction.png)

### Auctions you are in

Once you bid, the auction appears here with the item details and where the price has
reached.

![Active auctions](docs/05-active-auctions.png)

## How to run

You need Docker. Copy the example environment file and fill it in:

```bash
cd setup
cp .env.example .env
```

Then build and start everything:

```bash
./runscript.sh
```

The site is at `http://localhost:3309`. Create an account from the sign-in page, add an
item, then open an auction on it.

Every service waits for the database or broker it depends on, so a single
`docker compose up -d` brings the whole stack up in any order.

## Architecture

| Service | Port | Datastore | What it owns |
|---|---|---|---|
| frontend | 3309 | none | Flask templates and the browser-facing routes |
| items | 3307 | MySQL `itemsdb` | Item records, categories, reports |
| users | 3312 | MySQL `usersdb` | Accounts, login, admin flag |
| auctions | 3318 | MySQL `auctionsdb` | Auctions, bids, closing and winners |
| transactions | 3305 | MySQL `transactionsdb` | Cart and orders |
| watchlist | 3311 | MySQL `watchlistdb` | Items a user is following |
| messages | none | MongoDB `messagesmongo` | Support messages, email notifications |

The messaging service is reached over RabbitMQ instead of HTTP. Services call each
other by container name on the `netBackEnd` bridge network, and the frontend is the
only one published for a browser to reach directly.

## Correctness review

I went back through this project with the stack running and fixed the defects below.

**The build ignored the code in this repository.** Every Dockerfile ran
`git clone https://github.com/ntdai95/AuctionWebsite.git`, so the containers were built
from whatever sat on GitHub. Cloning this repository, changing a file and running the
setup gave you the old code with no warning. The source is copied in now, and the build
context is the repository root.

**Every base image was pinned to `latest`.** The stack built differently from one week
to the next, and that is what broke the message store: its data directory had been
written by an older `mongo:latest`, and a newer one refused to open it and exited. The
tags are fixed now.

**Five services died on a cold start.** Each Flask service opened its MySQL connection
at import time with no retry, and the two RabbitMQ consumers did the same with the
broker. On `docker compose up` they raised a connection error and exited, so the stack
came up with containers missing. The original setup script papered over this by
starting the databases alone and then sleeping for two minutes. Each service now waits
for its dependency, and all fourteen containers come up from one command.

**Seller controls were visible to everyone.** The admin flag is stored in
`localStorage`, which returns strings, so a normal user stored as `false` arrived back
as `"false"` and passed a truthy check. The close-auction panel rendered for every
signed-in user. Both places that read the flag now compare against the text.

**Logging out did not log you out.** The logout route redirected to the sign-in page
but nothing cleared the browser's stored identity, so the next page still treated you
as the previous user. Logging out now clears it.

**The watchlist link went nowhere.** The navigation bar had a watchlist entry that was
never given a URL.

**Two pages rendered blank cards.** Active auctions and my auctions were reading field
names the services do not return, such as `price` and `current_bid`, which Jinja
silently renders as empty strings. My auctions now reads the fields the endpoint
actually returns, and the active auctions route fetches the item name and the current
bid the way the auction page already did.

**The pages were not valid documents.** There was no doctype, headings sat inside
`<head>`, a form was never closed, element ids were duplicated across a loop, and one
id contained a space. The sign-in page loaded Bootstrap 4 while every other page loaded
Bootstrap 5, and it pulled in React 16, React 17, Babel and jQuery without using any of
them. There is a single layout now, one Bootstrap version, and a stylesheet.

**Placeholder text was shipping to users.** The navigation bar read `lol` until
JavaScript replaced it with `null | null` for signed-out visitors, the auction page
ended with a stray `just a test`, and several buttons were labelled with their quote
marks included, such as `'Buy now'`.

**Required fields were not required.** The create-item form put the `required`
attribute on the labels instead of the inputs, so only the price was enforced.

## What I would do next

Service addresses are hardcoded in the frontend templates as `localhost` URLs with port
numbers, which works for a local stack but not for a deployment. There is no
authentication between services, so any container on the network can call any endpoint.
The databases hold schema only, with no seed data, so a fresh stack starts empty.
None of the MySQL services declare a named volume either, so every
`docker compose down` discards the accounts, items and bids along with the containers.
