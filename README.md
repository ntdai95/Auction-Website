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
