from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_setup import Category, Base, Item, User

engine = create_engine('sqlite:///catalog.db',
                       connect_args={'check_same_thread': False})
Base.metadata.bind = engine
# Binding the engine to the metadata of the Base class so that the
# declaratives are accessed with a DBSession instance
DBSession = sessionmaker(bind=engine)
session = DBSession()
# A DBSession() instance establishes all conversations with the database
# and represents a "staging zone" for all the objects loaded into the
# database session object. Any change made against the objects in the
# session won't be persisted into the database until you call
# session.commit(). If you're not happy about the changes, you can
# revert all of them back to the last commit by calling
# session.rollback()

# Create a user
User1 = User(name="Bushra Safdar", email="bushra.m.safdar@gmail.com",
             picture="https://pbs.twimg.com/profile_images/2671170543\
                   /18debd694829ed78203a5a36dd364160_400x400.png")
session.add(User1)
session.commit()

# All items belonging to soccer category
category1 = Category(name="Soccer")
session.add(category1)
session.commit()

item1 = Item(user_id=1, name="Jersey", description="Jersey, in the Channel \
            Islands, was famous for its knitting trade in medieval times, \
            and because of that original fame, the name jersey is still \
            applied to many forms of knitted fabric, round or flat.",
             price="$3.99", category=category1)
session.add(item1)
session.commit()

item2 = Item(user_id=1, name="SoccerCleats", description=" The main purpose \
            of soccer shoes is to provide traction as you run. This is \
            usually accomplished by using cleats, except with indoor soccer\
            shoes that use textured rubber soles. Soccer cleats are usually \
            evenly spaced across the bottom of the shoe and spaced farther \
            apart than some other types of cleats.",
             price="$12.77", category=category1)
session.add(item2)
session.commit()

item3 = Item(user_id=1, name="Shin Guards", description="A shin guard or shin \
            pad is a piece of equipment worn on the front of a player's shin \
            to protect them from injury. These are commonly used in sports \
            including association football, baseball, ice hockey, \
            field hockey, lacrosse, cricket, mountain bike trials, \
            and other sports.", price="$4.5", category=category1)
session.add(item3)
session.commit()

# All items belonging to Basketball category
category2 = Category(name="BasketBall")
session.add(category2)
session.commit()


item4 = Item(user_id=1, name="Hoops", description="A backboard is a piece of \
            basketball equipment. It is a raised vertical board with an \
            attached basket consisting of a net suspended from a hoop. \
            It is usually rectangular as used in NBA, NCAA and \
            international basketball", price="$8.34", category=category2)
session.add(item4)
session.commit()

# All items belonging to Baseball category
category3 = Category(name="Baseball")
session.add(category3)
session.commit()

item5 = Item(user_id=1, name="Bat", description="A baseball bat is a smooth \
            wooden or metal club used in the sport of baseball to hit the \
            ball after it is thrown by the pitcher.", price="$2.99",
             category=category3)
session.add(item5)
session.commit()

# All items belonging to Frisbee category
category4 = Category(name="Frisbee")
session.add(category4)
session.commit()

item6 = Item(user_id=1, name="Frisbee", description="As the air flows over \
            the top of the frisbee, it speeds up and the pressure drops. \
            This creates lift.", price="$1.5", category=category4)
session.add(item6)
session.commit()

# All items belonging to Snowboarding category
category5 = Category(name="Snowboarding")
session.add(category5)
session.commit()

item7 = Item(user_id=1, name="Snowboard", description="Snowboard boots are \
            mostly considered soft boots, though alpine snowboarding uses a \
            harder boot similar to a ski boot. A boot's primary function is \
            to transfer the rider's energy into the board, protect the rider \
            with support, and keep the rider's feet warm.", price="$15",
             category=category5)
session.add(item7)
session.commit()

# All items belonging to Rock Climbing category
category6 = Category(name="Rock Climbing")
session.add(category6)
session.commit()

item8 = Item(user_id=1, name="Harness", description="A climbing harness is \
            an item of climbing equipment for rock-climbing, abseiling, or \
            other activities requiring the use of ropes to provide access or \
            safety such as industrial rope access, \
            working at heights etc.", price="$30.67", category=category6)
session.add(item8)
session.commit()


item9 = Item(user_id=1, name="Rope", description="Ropes used for climbing \
            are dynamic ropes, designed to stretch on impact to absorb the \
            energy generated by a fall. For most cragging and single pitch \
            climbing a single rope with a diameter of 10mm \
            is ideal.", price="$16.8", category=category6)
session.add(item9)
session.commit()


item10 = Item(user_id=1, name="Helmet", description="Climbing helmets are \
             designed to protect you against several common climbing \
             scenarios for example, when: rocks or hardware get kicked loose \
             above you. you peel off and whip into a wall. you hit your \
             head on an overhang.", price="$40.56", category=category6)
session.add(item10)
session.commit()

# All items belonging to Skating category
category7 = Category(name="Skating")
session.add(category7)
session.commit()

item11 = Item(user_id=1, name="Ice Skates", description="Ice skates are boots \
             with blades attached to the bottom, used to propel the bearer \
             across a sheet of ice while ice skating.", price="$34.45",
              category=category7)
session.add(item11)
session.commit()

# All items belonging to Hockey category
category8 = Category(name="Hockey")
session.add(category8)
session.commit()


item12 = Item(user_id=1, name="Stick", description="An ice hockey stick is a \
             piece of equipment used in ice hockey to shoot, pass, and carry \
             the puck across the ice.", price="$4.45", category=category8)
session.add(item12)
session.commit()


item13 = Item(user_id=1, name="Jersey", description="Traditional hockey \
             jerseys are oversized, roughly square, and made using fabrics \
             with limited elasticity.", price="$2.25", category=category8)
session.add(item13)
session.commit()

print "added catalog items!"
