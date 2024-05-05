import json

path = "../files/odds.json"

with open(path, 'r') as file:
    data = json.load(file)

def find_arbitrage(data):
    arbitrage_opportunities = []
    for game in data:
        odds_dict = {}
        bookmakers_dict = {}
        for bookmaker in game['bookmakers']:
            for market in bookmaker['markets']:
                if market['key'] == 'h2h':
                    for outcome in market['outcomes']:
                        team = outcome['name']
                        price = outcome['price']
                        if team not in odds_dict:
                            odds_dict[team] = []
                            bookmakers_dict[team] = []
                        odds_dict[team].append(price)
                        bookmakers_dict[team].append(bookmaker['title'])

        if len(odds_dict) == 2:
            team1, team2 = odds_dict.keys()
            for idx1, odd1 in enumerate(odds_dict[team1]):
                for idx2, odd2 in enumerate(odds_dict[team2]):
                    if (1 / odd1 + 1 / odd2) < 1:
                        arbitrage_opportunities.append({
                            'game': f"{game['home_team']} vs {game['away_team']}",
                            'team1': team1, 'odd1': odd1, 'bookmaker1': bookmakers_dict[team1][idx1],
                            'team2': team2, 'odd2': odd2, 'bookmaker2': bookmakers_dict[team2][idx2],
                            'arb_calc': 1 / odd1 + 1 / odd2
                        })

    return arbitrage_opportunities

arbitrage_results = find_arbitrage(data)

if len(arbitrage_results) > 0:
    for result in arbitrage_results:
        print(f"Arbitrage found in game {result['game']}:")
        print(f"  Bet on {result['team1']} at odds {result['odd1']} from {result['bookmaker1']}")
        print(f"  Bet on {result['team2']} at odds {result['odd2']} from {result['bookmaker2']}")
        print(f"  Arbitrage calculation: {result['arb_calc']:.4f}\n")
    
    with open('arbitrage_opportunities.json', 'w') as f:
        json.dump(arbitrage_results, f, indent=4)
else:
    print("No Arbitrage Opportunities")
