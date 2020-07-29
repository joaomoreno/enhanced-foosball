import random

class Narrator:
  def __init__(self):
    self.red = 0
    self.blue = 0
  
  def goal(self, red, blue):
    wasEqual = self.red == self.blue

    scorer = 'red' if red > self.red else 'blue'
    sufferer = 'blue' if red > self.red else 'red'
    scorerScore = red if red > self.red else blue
    suffererScore = blue if red > self.red else red

    self.red = red
    self.blue = blue

    if red == 7 or blue == 7:
      return random.choice([
        'END!',
        'gg',
      ])

    elif red == 0 and blue == 0:
      return random.choice([
        'gl hf',
        'Ready, set, go! 🔫 ',
        'Zero goals yet, better start hitting the ⚽!',
        'Good luck and fair play!'
      ])
    
    elif red == 6 and blue == 6:
      return random.choice([
        'Head to head on the last mile. 🏁 ',
        'Team %s equalizes, and this match goes for golden goal! ' % (scorer),
        'Strap yourselves in, we are going for final goal rush! ',
        'As they say in hockey: Sudden death is on! ',
        'High noon 🤠! ',
        'Sing along: It’s the final countdown – tadadadaa dadadida… '
      ])
    
    elif red == blue:
      return random.choice([
        'Reset! Both are %d goals away from the win!' % (7 - red),
        'Team %s just caught up by equalizing.' % (scorer),
        'This makes this a draw: The stands are in suspense!'
      ])
    
    elif red == 6 or blue == 6:
      winning = 'red' if red == 6 else 'blue'
      losing = 'blue' if red == 6 else 'red'
      return random.choice([
        'Goal! - Last chance for %s: Step it up! ' % (losing),
        'Oh, this pushes %s to the brink of defeat. Can they save themselves? ' % (losing),
        'Nearly there %s: Finish them! ' % (winning)
      ])

    elif wasEqual:
      return random.choice([
        '%s takes the lead! Gogo-goal! ' % (scorer),
        'Goal! Team %s is stepping it up.'  % (scorer),
        'Surprise - %s is one up already! ' % (scorer),
        'Watch out %s, don\'t let them get away!' % (sufferer)
      ])

    else:
      return random.choice([
        'Hello goalkeeper? Ball just passed by you!',
        'What a shot 🙀 - and it lands in the net!',
        'Congrats %s striker: This is a contender for goal of the week! 🏆 ' % (scorer),
        'Awesome shot! ✨ ',
        'You got this team %s: Push on!' % (scorer),
        'Goooooooooooooooooooooooal!',
        'Bot says: Foosball is best ball game.',
        'Team %s: score = score + 1' % (scorer),
        'Team %s: score++' % (scorer),
        'Team %s: score += 1' % (scorer)
      ])
