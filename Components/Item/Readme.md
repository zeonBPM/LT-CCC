# We are using the engine's classification until a better system is devised


# Advanced

# Aesthetic
### Map Blast SFX
Plays sound a single time per combat

# AOE
### Directer Shape AOE
Affects an area around the target according to the specified shape.  Will rotate based on target location.
### Rally AOE
Gives Blast AOE that affects allies but not the user
### Status Stacks On Hit
Target gains X stacks of the specified status on hit. Applies instantly, potentially causing values to change mid-combat
# Base

# Class_Change

# Custom
### Equippable Spell
This item will show up in the Spell menu, but is able to be manually equipped. If paired with the 'Force Equip On Use' component, it can manually and automatically be equipped

### Force Equip on Use
Forces the item to get equipped when used if it otherwise wouldn't be. Meant to be paired with the 'Equippable Spells' component, which by default are only equippable manually.

# Exp

# Extra

# Formula

# Special
### Rescue Unit
Rescues the target on hit
### Old Shove
Item shoves target on hit, ignores collisions. this is the old version of shove.
### Status Stacks On Hit
Target gains X stacks of the specified status on hit. Applies instantly, potentially causing values to change mid-combat.	has a SELF variant in the same file
### Deplete Accessory Use on Hit or Miss
The unit's accessory will lose one durability after hitting or missing

# Target
### Adjacent Empty Restrict
Prevents units from using this item if no adjacent squares are open
### Eval Target Only Restrict
Restricts which units or spaces can be targeted, but only calls once per target tile.


# Uses
### Eval HP Cost
Item subtracts the specified amount of HP upon use. If the subtraction would kill the unit the item becomes unusable.
### HP Cost as Uses
Display the HP Cost in place of Uses on the item. Do not combine with other uses components.
### Blank Uses
Display empty string in place of Uses on the item. Do not combine with other uses components



# Utility
### Eval Heal				
Heal the target based on an evaluation
### Eval Heal and Restore		
Heal the target based on an evaluation, and restores all negative statuses
### Spawn Region
Creates a region at the specified tile on hit
### Warp AI
Creates an AI usable warp staff


# Weapon
### Weapon TypeS		
Allows an item to have more than one weapon type
### Backfire Damage
Deals a certain amount of damage to the user.  Cannot be lethal
### Instakill
Item instantly kills the target with a specified probability
# Custom

### Weapon Type Exempt
Categorizes a weapon type but does not require the wielder to be able to use that weapon type
