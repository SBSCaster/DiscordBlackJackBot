from discord.ext import commands
import requests as rq
import json


class casino_bot(commands.Cog):
  def __init__(self, client):
    self.client = client
    self.deck = 'https://www.deckofcardsapi.com/api/deck/new/shuffle/?deck_count=1'
    self.deckid = ''
    self.dcount = 0
    self.dhand = []
    self.players = []
    self.player_hands = {}
    self.player_counts = {}
    self.staycount = 0
    
  
  @commands.command()
  async def register(self, ctx, name):
    self.players.append(name)
    await ctx.send('Player ' + name + ' has been registered')


  @commands.command()
  async def playhand(self, ctx):
    deck = json.loads(rq.get(self.deck).text)
    deckid = deck['deck_id']
    self.deckid = deckid
    dealer_cards = json.loads(rq.get('https://www.deckofcardsapi.com/api/deck/' + self.deckid + '/draw/?count=2').text)
    self.dhand = [dealer_cards['cards'][0], dealer_cards['cards'][1]]
    for player in self.players:
      cards = json.loads(rq.get('https://www.deckofcardsapi.com/api/deck/' + self.deckid + '/draw/?count=2').text)
      self.player_hands[player] = [cards['cards'][0], cards['cards'][1]]
    await ctx.send('DEALERS HAND;')
    await ctx.send("""
     .\n
    ////////////////////////////
    ///////////////////////////
    ///////////////////////////
    ///////////////////////////
    ///////////////////////////
    ///////////////////////////
    ///////////////////////////
    ///////////////////////////
    ///////////////////////////
    ///////////////////////////
    ///////////////////////////
    ///////////////////////////
    ///////////////////////////
    ///////////////////////////
    """)
    await ctx.send(self.dhand[1]['image'])
    for hand in self.player_hands.keys():
      await ctx.send(hand + "'s hand;")
      self.player_counts[hand] = 0
      for card in range(len(self.player_hands[hand])):
        await ctx.send(self.player_hands[hand][card]['image'])
        v1 = self.player_hands[hand][card]['value']
        if v1 == "KING" or v1 == "JACK" or v1 == "QUEEN":
          self.player_counts[hand] += 10
        elif v1 == "ACE":
          self.player_counts[hand] += 11
        else:
          self.player_counts[hand] += int(v1)
      await ctx.send(self.player_counts[hand])

    for card in self.dhand:
      if card['value'] == "KING" or card['value'] == 'JACK' or card['value'] == 'QUEEN':
        self.dcount += 10
      elif card['value'] == 'ACE':
        self.dcount += 11
      else:
        self.dcount += int(card['value'])
  

  async def dealerhit(self, ctx):
    new_card = json.loads(rq.get('https://www.deckofcardsapi.com/api/deck/' + 
    self.deckid + '/draw/?count=1').text)
    self.dhand.append(new_card['cards'][0])
    value = new_card['cards'][0]['value']
    if value == "KING" or value == "QUEEN" or value == "JACK":
      self.dcount += 10
    elif value == "ACE":
      self.dcount += 11
    else:
      self.dcount += int(value)
    

    

  @commands.command()
  async def hit(self, ctx, name):
    new_card = json.loads(rq.get('https://www.deckofcardsapi.com/api/deck/' + 
    self.deckid + '/draw/?count=1').text)
    self.player_hands[name].append(new_card['cards'][0])
    value = new_card['cards'][0]['value']
    if value == "KING" or value == "QUEEN" or value == "JACK":
      self.player_counts[name] += 10
    elif value == "ACE":
      self.player_counts[name] += 11
    else:
      self.player_counts[name] += int(value)
    await ctx.send(new_card['cards'][0]['image'])
    await ctx.send(self.player_counts[name])
    if self.player_counts[name] > 21:
      await ctx.send('Bust! whomp whomp')
      
  
  @commands.command()
  async def stay(self, ctx):
    self.staycount += 1
    winner = ['', 0]
    if self.staycount == len(self.players):
      while self.dcount < 21:
          await self.dealerhit(ctx=ctx)
          if self.dcount > 21:
            for card in self.dhand:
              await ctx.send(card['image'])
            await ctx.send('Oh no, something must have went wrong! I never bust..')
            break        
          if self.dcount == 21:
            for card in self.dhand:
              await ctx.send(card['image'])
            await ctx.send('21! The bot always wins!')
            break
          if self.dcount in range(17, 20):
            for card in self.dhand:
              await ctx.send(card['image'])
            await ctx.send(self.dcount)
            break
      for player in self.players:
        if self.player_counts[player] <= 21:
          if self.player_counts[player] > winner[1]:
            winner[0] = player
            winner[1] = self.player_counts[player]
      if self.dcount <= 21:
        if self.dcount > winner[1]:
          winner[0] = 'The Dealer'
          winner[1] = self.dcount
      await ctx.send(winner[0] + ' takes the pot with ' + str(winner[1]))

  @commands.command()
  async def fold(self, ctx):
    self.deckid = ''
    self.dcount = 0
    self.players = []
    self.dhand = []
    self.player_hands = {}
    self.player_counts = {}
    self.staycount = 0
    await ctx.send('I see, board cleared')

  


  

    


def setup(client):
  client.add_cog(casino_bot(client))
